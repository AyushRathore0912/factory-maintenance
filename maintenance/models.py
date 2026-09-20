from django.db import models
from django.contrib.auth.models import User


# ============================================================
# CATEGORY
# ============================================================

class Category(models.Model):

    name = models.CharField(
        max_length=100,
        unique=True
    )

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


# ============================================================
# SECTION / LINE
# ============================================================

class Section(models.Model):

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="sections"
    )

    name = models.CharField(
        max_length=100
    )

    class Meta:
        ordering = ["name"]

        constraints = [
            models.UniqueConstraint(
                fields=["category", "name"],
                name="unique_section_per_category"
            )
        ]

    def __str__(self):
        return f"{self.category.name} - {self.name}"


# ============================================================
# MACHINE
# ============================================================

class Machine(models.Model):

    STATUS_CHOICES = [
        ("ON", "ON"),
        ("OFF", "OFF"),
        ("MAINTENANCE", "Maintenance"),
    ]

    section = models.ForeignKey(
        Section,
        on_delete=models.CASCADE,
        related_name="machines"
    )

    name = models.CharField(
        max_length=100
    )

    description = models.CharField(
        max_length=255,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="OFF"
    )

    is_active = models.BooleanField(
        default=True
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


# ============================================================
# MACHINE STATUS LOG
# ============================================================

class MachineStatusLog(models.Model):

    machine = models.ForeignKey(
        Machine,
        on_delete=models.CASCADE,
        related_name="status_logs"
    )

    old_status = models.CharField(
        max_length=20,
        blank=True
    )

    new_status = models.CharField(
        max_length=20
    )

    changed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="machine_status_changes"
    )

    changed_at = models.DateTimeField(
        auto_now_add=True
    )

    remarks = models.TextField(
        blank=True
    )

    class Meta:
        ordering = ["-changed_at"]

    def __str__(self):
        return (
            f"{self.machine.name}: "
            f"{self.old_status} → {self.new_status}"
        )


# ============================================================
# BREAKDOWN
# ============================================================

class Breakdown(models.Model):

    STATUS_CHOICES = [
        ("OPEN", "Open"),
        ("IN_PROGRESS", "In Progress"),
        ("RESOLVED", "Resolved"),
    ]

    machine = models.ForeignKey(
        Machine,
        on_delete=models.CASCADE,
        related_name="breakdowns"
    )

    reported_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reported_breakdowns"
    )

    problem = models.TextField()

    solution = models.TextField(
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="OPEN"
    )

    start_time = models.DateTimeField()

    end_time = models.DateTimeField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return (
            f"{self.machine.name} - "
            f"{self.problem[:40]}"
        )

    @property
    def downtime_minutes(self):

        if not self.end_time:
            return None

        difference = self.end_time - self.start_time

        return int(
            difference.total_seconds() / 60
        )


# ============================================================
# BREAKDOWN HISTORY
# ============================================================

class BreakdownHistory(models.Model):

    breakdown = models.ForeignKey(
        Breakdown,
        on_delete=models.CASCADE,
        related_name="history"
    )

    action = models.CharField(
        max_length=255
    )

    remarks = models.TextField(
        blank=True
    )

    performed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="breakdown_actions"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return (
            f"{self.breakdown.machine.name} - "
            f"{self.action}"
        )


# ============================================================
# MIST INSPECTION
# ============================================================

class MISTInspection(models.Model):

    RESULT_CHOICES = [
        ("OK", "OK"),
        ("NOT_OK", "NOT OK"),
        ("NA", "N/A"),
    ]

    machine = models.ForeignKey(
        Machine,
        on_delete=models.CASCADE,
        related_name="mist_inspections"
    )

    inspected_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="mist_inspections"
    )

    result = models.CharField(
        max_length=10,
        choices=RESULT_CHOICES
    )

    remarks = models.TextField(
        blank=True
    )

    inspected_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-inspected_at"]

    def __str__(self):
        return (
            f"{self.machine.name} - "
            f"{self.result}"
        )