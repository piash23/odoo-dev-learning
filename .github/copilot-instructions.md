# Copilot Instructions for om_hospital (Odoo 13)

These instructions apply to this repository and should be followed for all code generation and refactoring.

## Project Context
- Odoo version: 13
- Module technical name: om_hospital
- Primary custom models follow hospital.* namespace (example: hospital.patient)

## General Coding Rules
- Follow existing repository naming and structure from NAMING_CONVENTIONS.md.
- Preserve existing code style and avoid unrelated refactors.
- Keep IDs and filenames predictable, descriptive, and snake_case.

## Model and Python Rules
- New model files must be in models/ and use snake_case names.
- Inherited standard models should use the original model name as file name (example: sale_order.py).
- Class names must be CamelCase.
- Prefer SQL constraints where possible for integrity.

## View and Action Rules
- View XML files go in views/ and use pattern: <model_name>_views.xml.
- Use standard ID prefixes:
  - action_<model>
  - view_<model>_form
  - view_<model>_tree
  - view_<model>_search
- Menu IDs use hospital_ prefix (example: hospital_menu_root).

## Report Rules (Odoo 13)
- Use report/ folder (singular), not reports/.
- Report XML files should use pattern: report/<model_snake_case>_report.xml.
- In Odoo 13, prefer <report .../> shortcut syntax.
- Recommended report action ID pattern: action_report_<model_snake_case>.
- Main QWeb template ID pattern: report_<model_snake_case>.
- report name/file must use: <module_name>.<main_template_id>
  - Example: om_hospital.report_hospital_patient
- Always declare report XML files in __manifest__.py under data.

## Custom Python Report Rules
- Use Python report class only when extra context/data is needed.
- Place Python report files under report/ with _report.py suffix.
- If Python report files exist:
  - import them in report/__init__.py
  - import report package in module root __init__.py
- Class must inherit models.AbstractModel.
- _name is mandatory and must be:
  - report.<module_name>.<main_template_id>
  - Example: report.om_hospital.report_hospital_patient
- Implement method exactly:
  - _get_report_values(self, docids, data=None)

## Required Module Structure Reminders
- Keep security/ir.model.access.csv present for model UI access.
- Keep data/ folder for sequences/demo/cron XML as needed.
- Ensure models/__init__.py imports all model files.

## Change Safety
- Do not remove existing behavior unless requested.
- Prefer minimal, targeted changes.
- If requirements conflict, follow convention.md in this repository.
