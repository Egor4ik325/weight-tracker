# Weight/food traker/webapp

> This project is still in development!

![Track page screenshot](screenshot.png)
![Database schema screenshot](schema.png)

## Features

- [x] Clean up code + style app & forms
- [x] Fix formsets create/update
- [ ] Validate product model


## Data model

Models:

- Food - abstract food
- Product - connects recipe to (of) food/recipe (adds real weight)
- Recipe - combination of products
- Record - eaten recipe with timestamp

## API

- create, list, update, delete food

- create, list, update, delete records (`/track/`)

## Automated Testing

Automanted e2e testing with Selenium for Firefox.

- Templates (HTML forms)

- Views (API)

- Forms (validation)

- Models (database)