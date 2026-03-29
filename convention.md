# Odoo Naming Conventions: om_hospital

This document outlines the coding standards and naming conventions used in the `om_hospital` module to ensure consistency, readability, and conflict prevention.

## 1. General Rules
* **Module Technical Name:** `om_hospital`
* **Module Namespace Prefix:** `hospital_` (used for global IDs like menus to prevent conflicts).
* **Inheritance Suffix:** `_hospital` (used to denote customizations made by this module).

---

## 2. Python Conventions (Models)

### A. Creating New Models
When creating a brand new model (e.g., `hospital.patient`).

| Element | Pattern | Example |
| :--- | :--- | :--- |
| **Model Name** | `[module].[model]` | `_name = 'hospital.patient'` |
| **Class Name** | CamelCase | `class HospitalPatient(models.Model):` |
| **File Name** | `models/[model_name_snake_case].py` | `models/hospital_patient.py` |

### B. Inheriting Existing Models
When modifying a standard Odoo model (e.g., `sale.order`).

| Element | Pattern | Example |
| :--- | :--- | :--- |
| **Inherit** | Same as original | `_inherit = 'sale.order'` |
| **Class Name** | Same as original | `class SaleOrder(models.Model):` |
| **File Name** | `models/[original_model_name].py` | `models/sale_order.py` |

### C. Class Structure & Method Ordering (New)
To maintain code cleanliness, class members must be ordered strictly as follows:

1.  **Private Attributes:** `_name`, `_description`, `_inherit`, `_rec_name`, `_order`.
2.  **Default Helper Methods:** methods used directly in field defaults (for example `_default_xxx`, `_get_default_xxx`).
3.  **Fields:** Database columns.
4.  **SQL Constraints:** `_sql_constraints` (typically placed after fields in Odoo core code).
5.  **`default_get`:** override for multi-field dynamic defaults.
6.  **Compute Methods:** `_compute_...` (usually with `@api.depends(...)`).
7.  **Onchange Methods:** `_onchange_...` with `@api.onchange(...)`.
8.  **Python Constraints:** `@api.constrains`.
9.  **CRUD Methods:** `create`, `write`, `unlink` (and other ORM overrides like `copy` when needed).
10. **Display/Search Methods:** `name_get`, `name_search`, `_name_search`.
11. **Action Methods:** Button actions (`action_...`).
12. **Other Public Business Methods:** methods called by cron/server actions/other models.
13. **Utility Methods:** shared helper/private methods (`_helper_...`, etc.).

**Note:** If a field uses `default=_my_method`, that method must appear before the field definition in Python class body order.
If you want to keep all methods below fields, use `default=lambda self: self._my_method()`.
`_sql_constraints` placement does not affect runtime behavior. In existing files, keep the file's current style and avoid pure style-only reordering.

### D. Method Terminology (Important)
These terms are commonly confused. Use the definitions below:

* **Default Methods**
    Methods that provide initial values when creating a record.
    Examples:
    * `default=lambda self: ...` on a field
    * `def _default_xxx(self): ...` used in field `default=_default_xxx`
    * `def default_get(self, fields_list): ...` for multi-field default logic
    Placement:
    * `_default_xxx`/`_get_default_xxx` used directly by fields should be before fields
    * `default_get` is recommended after fields (or immediately before fields if your team standard prefers it)

* **Compute Methods**
    Methods that calculate a field value dynamically via `compute='method_name'`.
    Typical naming: `_compute_xxx`.

* **`@api.depends(...)`**
    A dependency declaration for a compute method.
    In practice, methods with `@api.depends` are treated as compute methods because they recompute when dependent fields change.

* **Onchange Methods**
    UI/form helper methods (`@api.onchange`) that update values in the form before saving.
    They are not a replacement for compute or constraints.

* **Constraint Methods**
    Validation methods (`@api.constrains`) that block invalid data on create/write.

* **Display/Search Methods**
    Methods that control how records are shown and searched in relational fields.
    Examples:
    * `name_get`: controls display label
    * `name_search` / `_name_search`: controls autocomplete/search behavior

* **Other Common ORM Methods Often Missed**
    * `copy`: customize duplication behavior
    * `unlink`: delete behavior (already in CRUD)
    * `@api.ondelete`: pre-delete safety rules
    * computed field helpers: `inverse` and `search` methods when required

### E. Best Practices (New)
* **SQL Constraints:** Use `_sql_constraints` for data integrity (Unique, Check) whenever possible instead of Python code.
* **Images:** Use `fields.Image(...)` instead of `fields.Binary(...)` for automatic resizing.
* **Rec Name:** Do not define `_rec_name` if your model already has a `name` field.

---

## 3. XML Conventions (Views & Actions)

### A. File Naming
XML files should be located in the `views/` directory and match the Python file name, appended with `_views`.

* **Pattern:** `views/[model_name_snake_case]_views.xml`
* **Example:** `views/hospital_patient_views.xml`

### B. Defining New Views/Actions (IDs)
For new elements, we use the element type as the prefix. Odoo automatically namespaces these upon installation.

| Element | Pattern | Example ID |
| :--- | :--- | :--- |
| **Action** | `action_[model]` | `action_hospital_patient` |
| **Form View** | `view_[model]_form` | `view_hospital_patient_form` |
| **Tree View** | `view_[model]_tree` | `view_hospital_patient_tree` |
| **Search View** | `view_[model]_search` | `view_hospital_patient_search` |

### C. View Labeling / String Attributes (New)
Use proper singular/plural capitalization for the `string` attribute.

| View Type | Convention | Example Code |
| :--- | :--- | :--- |
| **Form** | **Singular** | `<form string="Patient">` |
| **Tree** | **Plural** | `<tree string="Patients">` |
| **Search**| **"Search" + Plural** | `<search string="Search Patients">` |

### D. Menus (IDs)
Menus are global elements, so we use the module name prefix to group them clearly in the database.

| Element | Pattern | Example ID |
| :--- | :--- | :--- |
| **Menu Root** | `[module]_menu_root` | `hospital_menu_root` |
| **Sub Menu** | `[module]_menu_[description]` | `hospital_menu_patient` |

### E. Inheriting Views (IDs)
When inheriting a view, use the standard Odoo ID pattern with a suffix to indicate the customization source.

| Element | Pattern | Example |
| :--- | :--- | :--- |
| **XML ID** | `view_[model]_form_inherit_[suffix]` | `id="view_sale_order_form_inherit_hospital"` |
| **View Name** | `[model].form.inherit.[module]` | `<field name="name">sale.order.form.inherit.om_hospital</field>` |
| **Inherit Ref** | `[orig_module].[orig_view_id]` | `ref="sale.view_order_form"` |

### F. Search View Best Practices (New)
* **Group By:** Modern Odoo (v14+) ignores the `expand="0"` attribute. It is acceptable to remove the `<group>` tag entirely if you simply want to list filters.
* **Separators:** Use `<separator/>` to visually group related filters.

---

## 4. Directory Structure

The module structure should strictly follow this hierarchy:

```text
om_hospital/
├── __init__.py
├── __manifest__.py
├── README.md                   # Project Documentation
├── NAMING_CONVENTIONS.md       # This file
├── models/
│   ├── __init__.py
│   ├── hospital_patient.py     # New Model (Strict naming)
│   └── sale_order.py           # Inherited Model
├── views/
│   ├── hospital_patient_views.xml # Views for New Model
│   ├── sale_order_views.xml       # Inherited Views
│   └── menu.xml                   # (Optional) Separated Menus
├── static/
│   └── description/
│       ├── index.html
│       └── icon.png
└── doc/                        # Extra documentation
    └── changelog.rst