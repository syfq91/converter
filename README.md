# Unit Converter

A tkinter-based unit converter for mm, inches, and feet.
<img width="850" height="474" alt="conv" src="https://github.com/user-attachments/assets/0e921757-2fe8-48cc-b482-e42676e9dbc2" />

## Usage

```bash
python3 converter.py
```

## Testing

Run unit tests for the core logic:

```bash
python3 test_converter.py
```

## Features

- Real-time conversion between mm, inches, and feet
- Supports positive and negative mixed dimensions (e.g., `7' 3 1/2"` or `-3 1/4"`)
- Smart typing validation (retains other field values while typing partial characters, clearing only on invalid inputs)
- Fraction-only input support (e.g., `1/2` or `1/2"`)
- Interactive clipboard copying with visual confirmation ("Copied!")
- Clear all fields with the "Clear" button or `Esc` key
- Responsive GUI layout with sensible minimum window sizing constraints
