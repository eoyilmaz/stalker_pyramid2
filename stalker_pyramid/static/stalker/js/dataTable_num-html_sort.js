// stalker_pyramid
// Copyright (C) 2013 Erkan Ozgur Yilmaz
//
// This file is part of stalker_pyramid.
//
// This library is free software; you can redistribute it and/or
// modify it under the terms of the GNU Lesser General Public
// License as published by the Free Software Foundation;
// version 2.1 of the License.
//
// This library is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
// Lesser General Public License for more details.
//
// You should have received a copy of the GNU Lesser General Public
// License along with this library; if not, write to the Free Software
// Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA

jQuery.extend( jQuery.fn.dataTableExt.oSort, {
    "num-html-pre": function (a) {
        'use strict';
        var x = String(a).replace(/<[\s\S]*?>/g, "");
        return parseFloat(x);
    },

    "num-html-asc": function (a, b) {
        'use strict';
        return ((a < b) ? -1 : ((a > b) ? 1 : 0));
    },

    "num-html-desc": function (a, b) {
        'use strict';
        return ((a < b) ? 1 : ((a > b) ? -1 : 0));
    }
});
