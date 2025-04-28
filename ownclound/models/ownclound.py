from odoo import models, fields, api, _
from nextcloud import NextCloud
import nextcloud_client
import requests
from requests.auth import HTTPBasicAuth
from odoo.exceptions import UserError, ValidationError

class OwncloudFolder(models.Model):

    _name = 'owncloud.folder'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Folder Name')
    user_id = fields.Many2one('res.users', string='Created By', default=lambda self: self.env.user)

    @api.model
    def create(self, vals):
        print('creating record -----')
        record = super(OwncloudFolder, self).create(vals)
        connector = self.env['owncloud.connector'].search([('active', '=', True)], limit=1)
        print(connector)
        connector.new_owncloud_folder(record.name)
        return record


class Owncloud(models.Model):

    _name = 'owncloud.connector'

    name = fields.Char('Description')
    domain = fields.Char('Domain')
    user_name = fields.Char('User Name')
    user_pwd = fields.Char('Password')
    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirm')], string='State')
    active = fields.Boolean('Active', default=True)

    def test_connection(self):
        self.ensure_one()
        if self.domain and self.user_pwd and \
                self.user_name:
            try:
                ncx = NextCloud(self.domain,
                                auth=HTTPBasicAuth(self.user_name,
                                                   self.user_pwd))

                data = ncx.list_folders('/').__dict__
                if data['raw'].status_code == 207:
                    return {
                        'type': 'ir.actions.client',
                        'tag': 'display_notification',
                        'params': {
                            'type': 'success',
                            'title': _("Connection Test Succeeded!"),
                            'message': _("Everything seems properly set up!"),
                            'sticky': False,
                        }
                    }
                else:
                    return {
                        'type': 'ir.actions.client',
                        'tag': 'display_notification',
                        'params': {
                            'type': 'danger',
                            'title': _("Connection Test Failed!"),
                            'message': _("An error occurred while testing the "
                                         "connection."),
                            'sticky': False,
                        }
                    }
            except Exception:
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'type': 'danger',
                        'title': _("Connection Test Failed!"),
                        'message': _("An error occurred while testing the "
                                     "connection."),
                        'sticky': False,
                    }
                }

    def reset_to_draft(self):
        self.ensure_one()
        self.state = 'draft'

    def new_owncloud_folder(self, folder_name):
        print('here is no calling')
        try:
            if self.domain and self.user_pwd and \
                    self.user_name:
                try:
                    # Connect to NextCloud using the provided username
                    # and password
                    ncx = NextCloud(self.domain,
                                    auth=HTTPBasicAuth(
                                        self.user_name,
                                        self.user_pwd))
                    # Connect to NextCloud again to perform additional
                    # operations
                    nc = nextcloud_client.Client(self.domain)
                    nc.login(self.user_name,
                             self.user_pwd)
                    # Get the folder name from the NextCloud folder ID
                    # If auto_remove is enabled, remove backup files
                    # older than specified days
                except Exception as error:
                    # rec.generated_exception = error
                    _logger.info('NextCloud Exception: %s', error)
                # Get the list of folders in the root directory of NextCloud

                data = ncx.list_folders('/').__dict__
                print(data)
                print(data['raw'].status_code, 'status code')
                folders = [
                    [file_name['href'].split('/')[-2],
                     file_name['file_id']]
                    for file_name in data['data'] if
                    file_name['href'].endswith('/')]
                # If the folder name is not found in the list of folders,
                # create the folder
                if folder_name not in [file[0] for file in folders]:
                    nc.mkdir(folder_name)
                else:
                    raise UserError(_('Folder with same name already existed !'))
        except UserError as error:
            raise UserError(f'{error}')
        except Exception:
            raise ValidationError('Please check connection')
