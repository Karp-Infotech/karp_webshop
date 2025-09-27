import uuid
import frappe
from frappe.sessions import Session as CoreSession
from frappe.utils import now
from frappe.auth import get_expiry_period

class CustomSession(CoreSession):
    def start(self):
        """start a new session with unique guest SID"""
        print("Custom Session id Generation")
        if self.user == "Guest":
            sid = "G-" + str(uuid.uuid4())
        else:
            sid = frappe.generate_hash()

        self.data.user = self.user
        self.sid = self.data.sid = sid
        self.data.data.user = self.user
        self.data.data.session_ip = frappe.local.request_ip

        if self.user != "Guest":
            self.data.data.update(
                {
                    "last_updated": now(),
                    "session_expiry": get_expiry_period(),
                    "full_name": self.full_name,
                    "user_type": self.user_type,
                }
            )

            # insert session
            self.insert_session_record()

            # update user login details
            user = frappe.get_doc("User", self.data["user"])
            user_doctype = frappe.qb.DocType("User")
            (
                frappe.qb.update(user_doctype)
                .set(user_doctype.last_login, now())
                .set(user_doctype.last_ip, frappe.local.request_ip)
                .set(user_doctype.last_active, now())
                .where(user_doctype.name == self.data["user"])
            ).run()

            user.run_notifications("before_change")
            user.run_notifications("on_update")
            frappe.db.commit()

