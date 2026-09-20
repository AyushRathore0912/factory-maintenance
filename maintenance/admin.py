from django.contrib import admin

from .models import (
    Category,
    Section,
    Machine,
    MachineStatusLog,
    Breakdown,
    BreakdownHistory,
    MISTInspection,
)


# ============================================================
# CATEGORY
# ============================================================

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = (
        "name",
    )

    search_fields = (
        "name",
    )

    ordering = (
        "name",
    )


# ============================================================
# SECTION
# ============================================================

@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "category",
    )

    list_filter = (
        "category",
    )

    search_fields = (
        "name",
        "category__name",
    )

    ordering = (
        "category",
        "name",
    )


# ============================================================
# MACHINE
# ============================================================

@admin.register(Machine)
class MachineAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "section",
        "status",
        "is_active",
    )

    list_filter = (
        "status",
        "is_active",
        "section__category",
    )

    search_fields = (
        "name",
        "description",
    )

    ordering = (
        "section__category",
        "section",
        "name",
    )


# ============================================================
# MACHINE STATUS LOG
# ============================================================

@admin.register(MachineStatusLog)
class MachineStatusLogAdmin(admin.ModelAdmin):

    list_display = (
        "machine",
        "old_status",
        "new_status",
        "changed_by",
        "changed_at",
    )

    list_filter = (
        "new_status",
        "changed_at",
    )

    search_fields = (
        "machine__name",
        "changed_by__username",
    )

    ordering = (
        "-changed_at",
    )


# ============================================================
# BREAKDOWN
# ============================================================

@admin.register(Breakdown)
class BreakdownAdmin(admin.ModelAdmin):

    list_display = (
        "machine",
        "status",
        "start_time",
        "end_time",
        "reported_by",
        "created_at",
    )

    list_filter = (
        "status",
        "start_time",
    )

    search_fields = (
        "machine__name",
        "problem",
        "solution",
    )

    ordering = (
        "-created_at",
    )


# ============================================================
# BREAKDOWN HISTORY
# ============================================================

@admin.register(BreakdownHistory)
class BreakdownHistoryAdmin(admin.ModelAdmin):

    list_display = (
        "breakdown",
        "action",
        "performed_by",
        "created_at",
    )

    list_filter = (
        "created_at",
    )

    search_fields = (
        "breakdown__machine__name",
        "action",
        "remarks",
    )

    ordering = (
        "-created_at",
    )


# ============================================================
# MIST INSPECTION
# ============================================================

@admin.register(MISTInspection)
class MISTInspectionAdmin(admin.ModelAdmin):

    list_display = (
        "machine",
        "result",
        "inspected_by",
        "inspected_at",
    )

    list_filter = (
        "result",
        "inspected_at",
    )

    search_fields = (
        "machine__name",
        "remarks",
        "inspected_by__username",
    )

    ordering = (
        "-inspected_at",
    )
    