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
2.  **SQL Constraints:** `_sql_constraints` (Placed before fields).
3.  **Fields:** Database columns.
4.  **Compute & Onchange Methods:** `_compute_...`, `_onchange_...`.
5.  **Python Constraints:** `@api.constrains`.
6.  **CRUD Methods:** `create`, `write`, `unlink`.
7.  **Action Methods:** Button actions.

### D. Best Practices (New)
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