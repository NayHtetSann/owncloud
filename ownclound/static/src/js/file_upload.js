odoo.define('owncloud.upload.file', function (require) {
"use strict";

    var core = require('web.core');
    var _t = core._t;

    var qweb = core.qweb;

    var UploadOwncloudFile = {

        start: function () {
            // define a unique uploadId and a callback method
            this.fileUploadID = _.uniqueId('account_bill_file_upload');
            $(window).on(this.fileUploadID, this._onFileUploaded.bind(this));
            return this._super.apply(this, arguments);
        },

        _onAddAttachment: function (ev) {
            // Auto submit form once we've selected an attachment
            var $input = $(ev.currentTarget).find('input.o_input_file');
            if ($input.val() !== '') {
                var $binaryForm = this.$('.o_owncloud_upload form.o_form_binary_form');
                $binaryForm.submit();
            }
        },

        _onFileUploaded: function () {
            // Callback once attachment have been created, create a bill with attachment ids
            var self = this;
            var attachments = Array.prototype.slice.call(arguments, 1);
            // Get id from result
            var attachent_ids = attachments.reduce(function(filtered, record) {
                if (record.id) {
                    filtered.push(record.id);
                }
                return filtered;
            }, []);
            return
//            return this._rpc({
//                model: 'account.journal',
//                method: 'create_invoice_from_attachment',
//                args: ["", attachent_ids],
//                context: this.initialState.context,
//            }).then(function(result) {
//                self.do_action(result);
//            });
        },

        _onUpload: function (event) {
            var self = this;
            // If hidden upload form don't exists, create it
            var $formContainer = this.$('.o_content').find('.o_owncloud_upload');
            if (!$formContainer.length) {
                $formContainer = $(qweb.render('owncloud.OwncloudHiddenUploadForm', {widget: this}));
                $formContainer.appendTo(this.$('.o_content'));
            }
            // Trigger the input to select a file
            this.$('.o_owncloud_upload .o_input_file').click();
        },
    }
    return UploadOwncloudFile;
});


odoo.define('owncloud.upload.tree', function (require) {
"use strict";
    var core = require('web.core');
    var FormController = require('web.FormController');
    var FormView = require('web.FormView');
    var UploadOwncloudFile = require('owncloud.upload.file');
    var viewRegistry = require('web.view_registry');

    var OwncloudFormController = FormController.extend(UploadOwncloudFile, {
        buttons_template: 'OwnCloudFormView.buttons',
        events: _.extend({}, FormController.prototype.events, {
            'click .o_button_upload_owncloud': '_onUpload',
            'change .o_owncloud_upload .o_form_binary_form': '_onAddAttachment',
        }),
    });

    var OwncloudFormView = FormView.extend({
        config: _.extend({}, FormView.prototype.config, {
            Controller: OwncloudFormController,
        }),
    });

    viewRegistry.add('owncloud_form', OwncloudFormView);
});