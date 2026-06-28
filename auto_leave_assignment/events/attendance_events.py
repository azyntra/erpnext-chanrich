"""
events/attendance_events.py
----------------------------
DocType event hook for Attendance.
Fires immediately when an Attendance record is submitted.
"""

import frappe
from auto_leave_assignment.core import assign_leave_for_attendance


def on_attendance_submit(doc, method=None):
    """
    Called automatically on Attendance submit (docstatus → 1).
    Delegates all logic to the core engine.
    called_from_scheduler=False so that Frappe manages the transaction.

    The skip_auto_leave flag is set by the bulk attendance import process
    to prevent the hook from firing during batch processing. The auto leave
    assignment is run explicitly after the full batch completes instead.
    """
    if getattr(doc.flags, "skip_auto_leave", False):
        return

    assign_leave_for_attendance(doc, called_from_scheduler=False)

