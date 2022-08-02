# -*- coding: utf-8 -*-
#############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2019-TODAY Cybrosys Technologies(<https://www.cybrosys.com>).
#    Author: Nishad (odoo@cybrosys.com)
#
#    You can modify it under the terms of the GNU AFFERO
#    GENERAL PUBLIC LICENSE (AGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU AFFERO GENERAL PUBLIC LICENSE (AGPL v3) for more details.
#
#    You should have received a copy of the GNU AFFERO GENERAL PUBLIC LICENSE
#    (AGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################
{
    'name': 'Commission Report',
    'version': '14.0.1.0.1',
    'summary': 'Module to generate Comission Report',
    'description': 'Module to generate Comission Report',
    'live_test_url': 'https://www.youtube.com/watch?v=7doVs8tDSnU&feature=youtu.be',
    'category': 'Extra Tools',
    'author': 'Rubixware S de RL de CV',
    'maintainer': 'Rubixware S de RL de CV',
    'company': 'Rubixware S de RL de CV',
    'website': 'https://www.rubixware.com',
    'depends': [
        'base','contacts'
        ],
    'data': [
        'views/partner.xml'
    ],
    'installable': True,
    'application': False,
    'auto_install': False
}
