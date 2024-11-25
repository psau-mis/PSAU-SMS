# Copyright 2015 LasLabs Inc.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

import logging
from datetime import datetime, timedelta

from werkzeug.exceptions import BadRequest

from odoo import http, _
from odoo.http import request
from odoo.exceptions import UserError

from odoo.addons.auth_signup.controllers.main import AuthSignupHome
from odoo.addons.web.controllers.home import ensure_db

_logger = logging.getLogger(__name__)


class PasswordSecurityHome(AuthSignupHome):
    def do_signup(self, qcontext):
        password = qcontext.get("password")
        user = request.env.user
        user._check_password(password)

        pass_min = user.company_id.password_minimum
        current_user = request.env['res.users'].sudo().search([('email', '=', qcontext.get('login'))], limit=1)
        write_date = current_user.password_write_date
        # print("Write Date:", write_date)
        # print("Password Time:", pass_min)
        # print("User:", qcontext.get('login'))
        if qcontext.get('reset_password_enabled'):
            if pass_min > 0:
                # Check if password write_date is available
                if write_date:
                    delta = timedelta(hours=pass_min)
                    # print("Delta:", delta)
                    # print("Delta + Write Date:", write_date+delta)
                    # print("Time Now:", datetime.now())
                    if password and write_date + delta > datetime.now():
                        raise UserError(
                            _("Passwords can only be reset every %d hour(s). Please contact an administrator for assistance.")
                            % pass_min
                        )
                    else:
                        write_date = datetime.now()
                        updated_time = {
                            'password_write_date': write_date,
                        }
                        current_user.write(updated_time)
                        # print("Updated Write Date:", write_date)
        return super(PasswordSecurityHome, self).do_signup(qcontext)

    # @http.route()
    # def web_login(self, *args, **kw):
    #     ensure_db()
    #     response = super(PasswordSecurityHome, self).web_login(*args, **kw)
    #     if not request.params.get("login_success"):
    #         return response
    #     if not request.env.user:
    #         return response
    #     # Now, I'm an authenticated user
    #     if not request.env.user._password_has_expired():
    #         return response
    #     # My password is expired, kick me out
    #     request.env.user.action_expire_password()
    #     request.session.logout(keep_db=True)
    #     # I was kicked out, so set login_success in request params to False
    #     request.params["login_success"] = False
    #     redirect = request.env.user.partner_id.signup_url
    #     return request.redirect(redirect)

    @http.route()
    def web_auth_signup(self, *args, **kw):
        """Try to catch all the possible exceptions not already handled in the parent method"""

        try:
            qcontext = self.get_auth_signup_qcontext()
        except Exception:
            raise BadRequest from None  # HTTPError: 400 Client Error: BAD REQUEST

        try:
            return super(PasswordSecurityHome, self).web_auth_signup(*args, **kw)
        except Exception as e:
            # Here we catch any generic exception since UserError is already
            # handled in parent method web_auth_signup()
            qcontext["error"] = str(e)
            response = request.render("auth_signup.signup", qcontext)
            response.headers["X-Frame-Options"] = "SAMEORIGIN"
            response.headers["Content-Security-Policy"] = "frame-ancestors 'self'"
            return response

    @http.route('/web/notice/reset_password', type='http', auth='user', website=True, sitemap=False)
    def web_notice_reset_password(self, *args, **kw):
        """route for the reset password notice when the password is nearing expiration"""
        qcontext = self.get_auth_signup_qcontext()
        
        login = request.env.user.login
        _logger.info(
            "Password reset attempt for <%s> by user <%s> from %s",
            login, request.env.user.login, request.httprequest.remote_addr)
        request.env['res.users'].sudo().reset_password(login)
        qcontext['message'] = _("Password reset instructions sent to your email")

        response = request.render('esmis_website_portal.portal_main_layout', qcontext)
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        response.headers['Content-Security-Policy'] = "frame-ancestors 'self'"
        return response