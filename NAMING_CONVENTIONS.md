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

### G. Header Button Naming Convention (New)
For form header buttons (`<header><button .../></header>`), use consistent action method names and user-facing labels.

| Button Purpose | Python Method (`name`) | UI Label (`string`) | Typical States |
| :--- | :--- | :--- | :--- |
| Confirm record | `action_confirm` | `Confirm` | `draft` |
| Mark finished | `action_done` | `Done` | `confirmed` |
| Cancel record | `action_cancel` | `Cancel` | `draft,confirmed` |
| Return to draft | `action_reset_to_draft` (preferred) or `action_reset` | `Reset to Draft` | `cancelled,done` |

Rules:
* Use `action_` prefix for button methods triggered with `type="object"`.
* Use a verb-based method name that describes the transition (`confirm`, `cancel`, `done`, `reset_to_draft`).
* Keep `string` short, title case, and business-friendly.
* Keep selection state keys stable and lowercase (`draft`, `confirmed`, `done`, `cancelled`).
* `oe_highlight` should be used only for the primary next action in a state.

Current `hospital.appointment` buttons already follow this convention. Optional improvement: rename `action_reset` to `action_reset_to_draft` for extra clarity.

### H. Report Conventions (Odoo 13)
Use a dedicated `report/` folder (singular) for report XML and optional report Python files.

Odoo 13 commonly defines report actions using the `<report .../>` tag (shortcut syntax). Keep this as the primary documented style in this project.

Version timeline for this convention:
* **Odoo 13:** `<report>` is the standard and recommended style.
* **Odoo 14:** shortcut tags (`<report>`, `<act_window>`) are deprecated; explicit `<record>` style with bindings is the recommended standard.
* **Odoo 15+:** shortcut tags still work for backward compatibility, but explicit `<record>` style is preferred.

#### Report File Naming
| Element | Pattern | Example |
| :--- | :--- | :--- |
| **Report XML File** | `report/[model_snake_case]_report.xml` | `report/hospital_patient_report.xml` |
| **Optional Report Python File** | `report/[model_snake_case]_report.py` | `report/hospital_patient_report.py` |

#### Report XML IDs and Fields (Using `<report>` Tag in Odoo 13)
| Element | Pattern | Example |
| :--- | :--- | :--- |
| **Report Action ID** | `action_report_[model_snake_case]` | `action_report_hospital_patient` |
| **Main Report Template ID** | `report_[model_snake_case]` | `report_hospital_patient` |
| **Optional Document Template ID** | `[main_template_id]_document` | `report_hospital_patient_document` |
| **`name` / `file` on `<report>`** | `[module_name].[main_template_id]` | `om_hospital.report_hospital_patient` |

Rules:
* Replace model dots with underscores in IDs (`hospital.patient` -> `hospital_patient`).
* Keep report actions prefixed with `action_report_` for clarity and consistency.
* In `<report>`, `name` must point to the main QWeb template external ID (`module.template_id`).
* Keep display `name` business-friendly (example: `Patient Details`).
* `print_report_name` should be readable and include the record name when useful.
* `file` should match `name` in standard QWeb PDF usage.
* Report XML files must be declared in `data` inside `__manifest__.py` or Odoo will not load them.

Accepted template structures:
* **Single-template report:** only `report_hospital_patient` template.
* **Two-template report:** `report_hospital_patient` (wrapper/loop) + `report_hospital_patient_document` (document body).

#### Custom Python Report Convention (`models.AbstractModel`)
Use a Python report class only when you need extra data preparation beyond plain `docs` rendering.

##### 1) Python File Name and Location
| Element | Rule | Example |
| :--- | :--- | :--- |
| **Folder** | Must be in `report/` | `om_hospital/report/` |
| **File Name** | Snake case, usually ending with `_report.py` | `hospital_patient_report.py` |

Notes:
* Import the file in `report/__init__.py`.
* Import the `report` package in the module root `__init__.py` when Python files exist under `report/`.

##### 2) Python Class Name
| Rule | Examples |
| :--- | :--- |
| CamelCase, include report intent | `PatientDetailsReport`, `ReportHospitalPatient` |

##### 3) Technical `_name` Rule (Mandatory)
This is a strict engine lookup rule, not only a style preference.

Pattern:
* `report.<module_name>.<main_template_id>`

Example:
* Module: `om_hospital`
* Main template ID: `report_hospital_patient`
* Required `_name`: `report.om_hospital.report_hospital_patient`

##### 4) Required Method Signature
Use exactly:
* `_get_report_values(self, docids, data=None)`

This method must return a dictionary used as QWeb rendering context.

##### 5) Example (Odoo 13)

File: `om_hospital/report/hospital_patient_report.py`

```python
from odoo import api, models


class PatientDetailsReport(models.AbstractModel):
    # CRITICAL: report.<module_name>.<main_template_id>
    _name = "report.om_hospital.report_hospital_patient"
    _description = "Patient Details Custom Report"

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env["hospital.patient"].browse(docids)
        total_appointments = self.env["hospital.appointment"].search_count([
            ("patient_id", "in", docids),
        ])

        return {
            "doc_ids": docids,
            "doc_model": "hospital.patient",
            "docs": docs,
            "custom_data": "This is a custom string",
            "total_appointments": total_appointments,
        }
```

##### 6) QWeb Usage of Returned Values
Any key returned by `_get_report_values` can be consumed in template XML.

```xml
<p>Total Appointments for these patients: <t t-esc="total_appointments"/></p>
```

##### 7) Checklist for Custom Reports
* [ ] File is under `report/` (example: `hospital_patient_report.py`).
* [ ] Class inherits `models.AbstractModel`.
* [ ] `_name` is exactly `report.<module_name>.<main_template_id>`.
* [ ] Method is exactly `_get_report_values(self, docids, data=None)`.
* [ ] Python file is imported in `report/__init__.py`.
* [ ] `report` package is imported in module root `__init__.py`.

Recommended action snippet (Odoo 13, preferred):

```xml
<report
    id="action_report_hospital_patient"
    model="hospital.patient"
    string="Patient Details"
    report_type="qweb-pdf"
    name="om_hospital.report_hospital_patient"
    file="om_hospital.report_hospital_patient"
/>
```

Alternative verbose form (also valid in Odoo 13, and preferred for Odoo 14+):

```xml
<record id="action_report_hospital_patient" model="ir.actions.report">
    <field name="name">Patient Details</field>
    <field name="model">hospital.patient</field>
    <field name="report_type">qweb-pdf</field>
    <field name="report_name">om_hospital.report_hospital_patient</field>
    <field name="report_file">om_hospital.report_hospital_patient</field>
    <field name="binding_model_id" ref="model_hospital_patient"/>
    <field name="binding_type">report</field>
</record>
```

---

## 4. Sequence Conventions

When defining `ir.sequence` records, keep ID/code naming deterministic and avoid ambiguous suffixes.

Hard rule:
* The sequence `code` value must never end with `.code`.

### A. Standard Sequences (Single-Use Models)
Use this pattern when one model uses a single sequence stream.

| Element | Pattern | Example |
| :--- | :--- | :--- |
| **Sequence ID** | `seq_[model_snake_case]` | `seq_hospital_patient` |
| **Sequence Code** | `[model]` | `hospital.patient` |

### B. Contextual Sequences (Multi-Use Models)
Use this pattern when one model has distinct sequence streams by business context (for example inpatient/outpatient).

| Element | Pattern | Example |
| :--- | :--- | :--- |
| **Sequence ID** | `seq_[model_snake_case]_[context]` | `seq_hospital_appointment_inpatient` |
| **Sequence Code** | `[model].[context]` | `hospital.appointment.inpatient` |

Note:
* For strictly categorized models, skip creating a base sequence and create only contextual sequences.

### C. Sequence Data XML Conventions (`data/hospital_sequence_data.xml`)
Use these rules for the `<record model="ir.sequence">` entries inside sequence data files.

| Element | Standard Pattern | Contextual Pattern | Example |
| :--- | :--- | :--- | :--- |
| **XML Record ID (`id`)** | `seq_[model_snake_case]` | `seq_[model_snake_case]_[context]` | `seq_hospital_patient`, `seq_hospital_appointment_inpatient` |
| **Sequence Code (`<field name="code">`)** | `[model]` | `[model].[context]` | `hospital.patient`, `hospital.appointment.inpatient` |

Rules:
* Keep XML `id` and sequence `code` semantically aligned (same model and same optional context).
* Do not use `.code` suffix in `code` values (invalid style example: `hospital.patient.code`).

Minimal examples:

```xml
<record id="seq_hospital_patient" model="ir.sequence">
    <field name="name">Patient</field>
    <field name="code">hospital.patient</field>
    <field name="prefix">HP</field>
    <field name="padding">5</field>
</record>

<record id="seq_hospital_appointment_inpatient" model="ir.sequence">
    <field name="name">Inpatient Appointment</field>
    <field name="code">hospital.appointment.inpatient</field>
    <field name="prefix">INP</field>
    <field name="padding">5</field>
</record>
```

---

## 5. Directory Structure

The module structure should strictly follow this hierarchy:

```text
om_hospital/
├── __init__.py
├── __manifest__.py
├── README.md                   # Project Documentation
├── NAMING_CONVENTIONS.md       # This file
├── security/
│   └── ir.model.access.csv     # Required ACLs for UI/model access
├── data/
│   ├── hospital_sequence_data.xml # (Optional) Sequences (example: patient IDs)
│   └── hospital_cron_data.xml     # (Optional) Scheduled actions
├── demo/
│   └── hospital_demo_data.xml     # (Optional) Demo records (non-production seed data)
├── models/
│   ├── __init__.py             # Required to load Python model files
│   ├── hospital_patient.py     # New Model (Strict naming)
│   └── sale_order.py           # Inherited Model
├── report/
│   ├── hospital_patient_report.xml # Patient report definition (QWeb + action)
│   ├── hospital_appointment_report.xml # (Optional) Appointment-focused report
│   ├── hospital_patient_report.py # (Optional) report helper/parser
│   └── __init__.py                # Required when Python files are used in report/
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
```

Data loading note:
* Demo data files must live in `demo/` and must be loaded from the `demo`: [] array in `__manifest__.py`.
* Never load demo data files from the `data`: [] array, to avoid installing fake/demo records in production databases.

---

## 6. Demo Data Conventions

Demo data (test/seed records) must be isolated from production data and stored separately in the `demo/` folder.

### A. File Naming
Demo data XML files should use a descriptive pattern that clarifies what data they contain.

| Element | Pattern | Example |
| :--- | :--- | :--- |
| **Demo Data File** | `demo/[module]_[model(s)]_demo.xml` or `demo/[module]_demo_data.xml` | `demo/hospital_patient_appointment_demo.xml` or `demo/hospital_demo_data.xml` |

Rules:
* Keep the file name concise and descriptive.
* Group related models (e.g., patient + appointment) in one file for cohesion, or split if they grow large.
* Prefix with module name to avoid conflicts.

### B. Record ID Convention (Demo Records)
Use descriptive, human-readable IDs for demo records to make them easy to identify and reference.

| Model | ID Pattern | Example |
| :--- | :--- | :--- |
| **hospital.patient** | `hospital_patient_demo_[descriptor]` | `hospital_patient_demo_john_doe`, `hospital_patient_demo_patient_001` |
| **hospital.appointment** | `hospital_appointment_demo_[descriptor]` | `hospital_appointment_demo_john_checkup`, `hospital_appointment_demo_inpatient_001` |

Rules:
* Use descriptive identifiers (names, types) rather than generic numbers.
* Maintain consistency across your demo set.
* Make IDs human-readable so developers quickly understand what each record represents.

### C. Demo Data XML Structure

Key rules:
* Wrap demo records in `<data noupdate="0">` (not `noupdate="1"`). This allows demo data to be refreshed on module updates.
* Use `<record>` elements with model attribute matching your model name.
* Reference related demo records using `ref="demo_record_id"` in relational fields.
* Group by model for clarity (patients first, then appointments referencing patients).

### D. Example: hospital_demo_data.xml

```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data noupdate="0">
        
        <!-- Hospital Patient Demo Records -->
        <record id="hospital_patient_demo_john_doe" model="hospital.patient">
            <field name="name">John Doe</field>
            <field name="patient_id">PAT/00001</field>
            <field name="age">35</field>
            <field name="gender">male</field>
            <field name="blood_group">O+</field>
            <field name="mobile">+1-555-0101</field>
            <field name="email">john.doe@example.com</field>
        </record>

        <record id="hospital_patient_demo_jane_smith" model="hospital.patient">
            <field name="name">Jane Smith</field>
            <field name="patient_id">PAT/00002</field>
            <field name="age">28</field>
            <field name="gender">female</field>
            <field name="blood_group">AB-</field>
            <field name="mobile">+1-555-0102</field>
            <field name="email">jane.smith@example.com</field>
        </record>

        <!-- Hospital Appointment Demo Records (Referencing Patients) -->
        <record id="hospital_appointment_demo_john_checkup" model="hospital.appointment">
            <field name="name">Routine Checkup</field>
            <field name="patient_id" ref="hospital_patient_demo_john_doe"/>
            <field name="appointment_date">2025-04-10 09:00:00</field>
            <field name="appointment_type">inpatient</field>
            <field name="description">Regular annual checkup for patient</field>
            <field name="state">draft</field>
        </record>

        <record id="hospital_appointment_demo_jane_surgery" model="hospital.appointment">
            <field name="name">Pre-Surgery Consultation</field>
            <field name="patient_id" ref="hospital_patient_demo_jane_smith"/>
            <field name="appointment_date">2025-04-12 14:30:00</field>
            <field name="appointment_type">outpatient</field>
            <field name="description">Consultation before scheduled surgery</field>
            <field name="state">draft</field>
        </record>

    </data>
</odoo>
```

### E. __manifest__.py Configuration

Ensure demo data is loaded in the correct array:

```python
{
    'name': 'Hospital Management',
    'version': '13.0.1.0.0',
    'category': 'Healthcare',
    'author': 'Your Name',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'data/hospital_sequence_data.xml',
    ],
    'demo': [
        'demo/hospital_demo_data.xml',  # Demo records HERE, not in 'data'
    ],
    'installable': True,
}
```

Critical rule:
* Demo files go in `'demo': []` array ONLY.
* Production data (sequences, crons, access rules) goes in `'data': []` array.

### F. Best Practices for Demo Data

1. **Isolation:** Demo records should never interfere with production workflows.
2. **Realistic Values:** Use realistic but clearly identifiable test data (e.g., `john_doe`, not `xxx`).
3. **Relationships:** Always use `ref="demo_record_id"` to link related demo records.
4. **Minimal Set:** Include just enough demo records to showcase module functionality (3-5 records typically).
5. **States:** Place demo records in meaningful initial states (`draft`, `confirmed`, etc.) so they demonstrate realistic workflows.
6. **Cleanups:** noupdate="0" ensures demo data is refreshed on module updates/reinstalls (useful for testing).

---

## 7. Master Data Conventions

Master data (reference/configuration records) are production-critical records that should persist across module updates and never be deleted. Examples: appointment types, patient categories, facility types—similar to Odoo's "Chart of Accounts."

### A. Master Data vs Demo Data

**Master Data** is distinct from demo data:

| Aspect | Master Data | Demo Data |
| :--- | :--- | :--- |
| **Purpose** | System reference/configuration for production | Test/example records for development |
| **Folder** | `data/` | `demo/` |
| **Array in __manifest__.py** | `'data': [...]` | `'demo': [...]` |
| **noupdate flag** | `noupdate="1"` | `noupdate="0"` |
| **Behavior on Update** | Persists (never overwritten) | Refreshed on reinstall |
| **User-facing?** | YES - users select these in forms | NO - temporary test data |
| **Example** | Appointment types (Inpatient, Outpatient) | Sample patient "John Doe" |

### B. File Naming for Master Data

| Element | Pattern | Example |
| :--- | :--- | :--- |
| **Master Data File** | `data/[model_snake_case]_data.xml` | `data/hospital_appointment_type_data.xml`, `data/hospital_patient_category_data.xml` |

Breakdown:
- `data/` — Folder where master data lives
- `[model_snake_case]` — Your model name in snake_case: e.g., `hospital_appointment_type`, `hospital_patient_category`
- `_data.xml` — Suffix to indicate this file contains master records

You can split master data across multiple files (one per model type) or combine related ones.

### C. Master Data Record ID Naming Convention

**ID Pattern:**
```
[model_snake_case]_[code]
```

**Component Breakdown:**

| Component | Meaning | Rules | Example |
| :--- | :--- | :--- | :--- |
| `[model_snake_case]` | Your model name in snake_case | Lowercase snake_case (mirrors your model name) | `hospital_appointment_type`, `hospital_patient_category`, `hospital_facility_type` |
| `[code]` | Unique identifier for this record | Lowercase snake_case, stable, self-documenting | `inpatient`, `vip`, `emergency` |

**Why this pattern?** Using the model name directly (instead of module + entity_type) avoids repetition in XML references. This keeps `self.env.ref()` calls clean: `self.env.ref('om_hospital.hospital_patient_category_vip')` instead of the redundant `self.env.ref('om_hospital.om_hospital_hospital_patient_category_vip')`.

**Full Examples:**

| Entity | ID | Breakdown | Python Ref |
| :--- | :--- | :--- | :--- |
| Inpatient Appointment Type | `hospital_appointment_type_inpatient` | `hospital_appointment_type` + `inpatient` | `self.env.ref('om_hospital.hospital_appointment_type_inpatient')` |
| VIP Patient Category | `hospital_patient_category_vip` | `hospital_patient_category` + `vip` | `self.env.ref('om_hospital.hospital_patient_category_vip')` |
| ICU Facility | `hospital_facility_type_icu` | `hospital_facility_type` + `icu` | `self.env.ref('om_hospital.hospital_facility_type_icu')` |
| Emergency Appointment | `hospital_appointment_type_emergency` | `hospital_appointment_type` + `emergency` | `self.env.ref('om_hospital.hospital_appointment_type_emergency')` |

**Critical Rules:**

1. **Stable IDs:** Never change an ID once it's released. Other modules may reference it using `ref=`.
2. **Lowercase snake_case:** Always use lowercase and underscores (no spaces, no camelCase, no hyphens).
3. **Self-documenting:** The ID should tell you what the record is without looking at the code.
4. **Unique across module:** No two master records should have the same ID in your module.
5. **Never use timestamps or numbers as codes:** Use meaningful descriptors that survive version upgrades.

### D. Master Data XML Structure

Key rules:
* Wrap records in `<data noupdate="1">` (persists across updates).
* Group by entity type for clarity.
* Use stable, human-readable field names and values.
* Do NOT use `ref="..."` to external model records unless they're from `base` Odoo (e.g., `ref="base.user_root"`).

### E. Example: hospital_appointment_type_data.xml

```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data noupdate="1">
        
        <!-- Appointment Types - Master Data (System Reference) -->
        <record id="hospital_appointment_type_inpatient" model="hospital.appointment.type">
            <field name="name">Inpatient</field>
            <field name="code">inpatient</field>
            <field name="description">Patient admitted to hospital for treatment</field>
            <field name="sequence">10</field>
            <field name="active">True</field>
        </record>

        <record id="hospital_appointment_type_outpatient" model="hospital.appointment.type">
            <field name="name">Outpatient</field>
            <field name="code">outpatient</field>
            <field name="description">Patient visits clinic without admission</field>
            <field name="sequence">20</field>
            <field name="active">True</field>
        </record>

        <record id="hospital_appointment_type_emergency" model="hospital.appointment.type">
            <field name="name">Emergency</field>
            <field name="code">emergency</field>
            <field name="description">Emergency/urgent care appointment</field>
            <field name="sequence">5</field>
            <field name="active">True</field>
        </record>

    </data>
</odoo>
```

### F. Example: hospital_patient_category_data.xml

```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>
    <data noupdate="1">
        
        <!-- Patient Categories - Master Data (System Reference) -->
        <record id="hospital_patient_category_regular" model="hospital.patient.category">
            <field name="name">Regular</field>
            <field name="code">regular</field>
            <field name="description">Standard patient category</field>
            <field name="sequence">20</field>
        </record>

        <record id="hospital_patient_category_vip" model="hospital.patient.category">
            <field name="name">VIP</field>
            <field name="code">vip</field>
            <field name="description">VIP/Premium patient category</field>
            <field name="sequence">10</field>
        </record>

        <record id="hospital_patient_category_insurance" model="hospital.patient.category">
            <field name="name">Insurance</field>
            <field name="code">insurance</field>
            <field name="description">Patient covered by insurance</field>
            <field name="sequence">15</field>
        </record>

    </data>
</odoo>
```

### G. __manifest__.py Configuration

Ensure master data is loaded in the `'data': []` array:

```python
{
    'name': 'Hospital Management',
    'version': '13.0.1.0.0',
    'category': 'Healthcare',
    'author': 'Your Name',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'data/hospital_sequence_data.xml',           # Sequences (production)
        'data/hospital_appointment_type_data.xml',   # Master data
        'data/hospital_patient_category_data.xml',   # Master data
    ],
    'demo': [
        'demo/hospital_demo_data.xml',  # Demo records for testing
    ],
    'installable': True,
}
```

### H. When to Use Master Data vs Demo Data

**Master Data (Production) — Goes in `data/` folder:**
* Appointment types, patient categories, facility classifications
* Configuration records that users rely on in daily workflows
* Reference data that should never be deleted
* Use `noupdate="1"` to prevent overwriting on updates
* Users will select these in dropdown fields

**Demo Data (Testing) — Goes in `demo/` folder:**
* Sample patients, sample appointments
* Test records to showcase module functionality
* Records that can be safely deleted during development
* Use `noupdate="0"` to refresh on reinstall
* Not visible to end users on production

### I. Best Practices for Master Data

1. **Stability:** IDs must never change once published (other modules may reference them).
2. **Meaningful Sequences:** Use `sequence` field so users can reorder in UI if needed.
3. **Active Flag:** Always include `<field name="active">True</field>` for visibility.
4. **Documentation:** Add `description` field to clarify purpose to end users.
5. **Minimal Set:** Only include categories/types that are truly essential and universally applicable.
6. **No User Data:** Master data should NOT contain user-specific information (e.g., "John Doe" patient belongs in demo, not master data).

---

## 4. Security Conventions

All security configurations belong in a single `security/hospital_security.xml` file. This file defines user groups, permission categories, and access control rules for the module.

### A. File Structure and Location

| Element | Pattern | Example |
| :--- | :--- | :--- |
| **Security XML File** | `security/hospital_security.xml` | Located in `addons/om_hospital/security/` |
| **Access Control CSV** | `security/ir.model.access.csv` | For model-level CRUD permissions |

**Note:** Security files must be declared in `__manifest__.py` under `data`, before or after the access CSV (convention: list security XML after CSV).

### B. Module Category (Security Group Category)

Module categories help organize groups in Settings > Users & Companies > Groups. Use this to visually group your module's roles.

| Element | Pattern | Example |
| :--- | :--- | :--- |
| **XML ID** | `module_category_[description]` | `module_category_hospital` |
| **Display Name** | Title Case, descriptive | `Hospital Management` |
| **Model** | Always `ir.module.category` | `<record model="ir.module.category">` |

**Example:**
```xml
<record id="module_category_hospital" model="ir.module.category">
    <field name="name">Hospital Management</field>
    <field name="description">Category for Hospital Module</field>
    <field name="sequence">1</field>
</record>
```

### C. User Groups (Roles)

Define functional roles (Doctor, Manager, etc.) that users can be assigned to. Each group grants specific permissions and rules.

| Element | Pattern | Example |
| :--- | :--- | :--- |
| **XML ID** | `group_[module]_[role_name]` | `group_hospital_doctor` |
| **Display Name** | Title Case, single word role | `Doctor` |
| **Model** | Always `res.groups` | `<record model="res.groups">` |
| **Category Ref** | Reference to module category | `ref="module_category_hospital"` |

**Rules:**
* Always inherit from `base.group_user` (or chain inheritance through other groups for role hierarchy).
* Use `implied_ids` to establish role hierarchy (e.g., Manager implies Doctor permissions).
* Group names should be **singular and role-focused** (not "Doctors", use "Doctor").
* Keep the display name concise for UI clarity in user forms.

**Example:**
```xml
<record id="group_hospital_doctor" model="res.groups">
    <field name="name">Doctor</field>
    <field name="implied_ids" eval="[(4, ref('base.group_user'))]"/>
    <field name="category_id" ref="module_category_hospital"/>
</record>

<record id="group_hospital_manager" model="res.groups">
    <field name="name">Manager</field>
    <field name="implied_ids" eval="[(4, ref('group_hospital_doctor'))]"/>
    <field name="category_id" ref="module_category_hospital"/>
</record>
```

### D. Access Control Rules (ir.rule)

Record Rules define domain-based record filtering for groups. They control which records each group can see and edit.

| Element | Pattern | Example |
| :--- | :--- | :--- |
| **XML ID** | `rule_[model]_[description]` | `rule_hospital_patient_doctor_own` |
| **Display Name** | Clear description of the rule | `Doctor can only see their own patients` |
| **Model** | Always `ir.rule` | `<record model="ir.rule">` |
| **Target Model Ref** | Reference to the model being restricted | `ref="model_hospital_patient"` |

**Field Reference:**
* `model_id` → Use `ref="model_[model_name]"` where underscores replace dots (e.g., `model_hospital_patient` for `hospital.patient`).
* `groups` → Specify which groups this rule applies to using `eval="[(4, ref('group_id'))]"` syntax.
* `domain_force` → Write the domain using model field paths (e.g., `[('doctor_id.related_user_id', '=', user.id)]`).
* `perm_read`, `perm_write`, `perm_create`, `perm_unlink` → Set to `1` (allow) or `0` (deny); omit for no restriction.

**Example:**
```xml
<record id="rule_hospital_patient_doctor_own" model="ir.rule">
    <field name="name">Doctor can only see their own patients</field>
    <field name="model_id" ref="model_hospital_patient"/>
    <field name="groups" eval="[(4, ref('group_hospital_doctor'))]"/>
    <field name="domain_force">[('doctor_id.related_user_id', '=', user.id)]</field>
</record>
```

### E. Model Access CSV (ir.model.access)

The `ir.model.access.csv` file grants or denies model-level CRUD permissions (Create, Read, Update, Delete) to groups.

**CSV Header:**
```
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
```

| Column | Pattern | Example |
| :--- | :--- | :--- |
| **id** | `access_[model_name]` | `access_hospital_patient` |
| **name** | Descriptive label (info only) | `access.hospital.patient` |
| **model_id:id** | `model_[model_name]` | `model_hospital_patient` |
| **group_id:id** | Group reference or `base.group_user` for all users | `base.group_user` |
| **perm_read** | `1` (allow) or `0` (deny) | `1` |
| **perm_write** | `1` (allow) or `0` (deny) | `1` |
| **perm_create** | `1` (allow) or `0` (deny) | `1` |
| **perm_unlink** | `1` (allow) or `0` (deny) | `1` |

**Example:**
```csv
id,name,model_id:id,group_id:id,perm_read,perm_write,perm_create,perm_unlink
access_hospital_patient,access.hospital.patient,model_hospital_patient,base.group_user,1,1,1,1
access_hospital_doctor,access.hospital.doctor,model_hospital_doctor,base.group_user,1,1,1,1
```

### F. Security Conventions Best Practices

1. **Hierarchy:** Use implied_ids to create role hierarchies (e.g., Manager > Doctor > Base User).
2. **Rule Domain Paths:** Always validate domain paths match actual model field names (e.g., `related_user_id`, not `user_id`).
3. **Group Naming:** Use singular, role-focused names that clearly describe the user's function.
4. **Rule Descriptions:** Keep rule names descriptive so administrators understand the purpose.
5. **Access Order:** Declare access control in `__manifest__.py` after groups are defined in `hospital_security.xml`.
6. **Testing:** Always test rules with sample users from each group to confirm filtering works as expected.
7. **Documentation:** Add inline comments in `hospital_security.xml` for complex rules or hierarchies.

### G. Complete Example (hospital_security.xml)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<odoo>
    <!-- Security Category -->
    <record id="module_category_hospital" model="ir.module.category">
        <field name="name">Hospital Management</field>
        <field name="description">Category for Hospital Module</field>
        <field name="sequence">1</field>
    </record>

    <!-- User Groups (Roles) -->
    <record id="group_hospital_doctor" model="res.groups">
        <field name="name">Doctor</field>
        <field name="implied_ids" eval="[(4, ref('base.group_user'))]"/>
        <field name="category_id" ref="module_category_hospital"/>
    </record>

    <record id="group_hospital_manager" model="res.groups">
        <field name="name">Manager</field>
        <field name="implied_ids" eval="[(4, ref('group_hospital_doctor'))]"/>
        <field name="category_id" ref="module_category_hospital"/>
    </record>

    <!-- Record Rules (Access Control) -->
    <record id="rule_hospital_patient_doctor_own" model="ir.rule">
        <field name="name">Doctor can only see their own patients</field>
        <field name="model_id" ref="model_hospital_patient"/>
        <field name="groups" eval="[(4, ref('group_hospital_doctor'))]"/>
        <field name="domain_force">[('doctor_id.related_user_id', '=', user.id)]</field>
    </record>
</odoo>
```
7. **Testing Impact:** Master data persists across test runs—ensure it doesn't interfere with test workflows.