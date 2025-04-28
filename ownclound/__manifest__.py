# Copyright 2022 CreuBlanca
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Owncloud Integration",
    "summary": """
        Allow to create folder and upload file to related folder of owncloud""",
    "version": "14.0.1.0",
    "license": "AGPL-3",
    "author": "NHS",
    "website": "",
    "depends": ["base", "mail"],
    "data": [
        "security/ir.model.access.csv",
        "views/owncloud.xml",
        "views/owncloud_view.xml",
    ],
    'qweb': [
        "static/src/xml/file_upload_view.xml",
    ],
}
