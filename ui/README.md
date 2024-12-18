# Okto-Ui

## Features
- **Nuxt 3 Framework**
- **PrimeVue Integration** for modern UI components.
- **Tailwind CSS** for utility-first styling.
- Configurable layout and menu through `layouts/` and `pages/`.
- Easily extendable and customizable.

## Getting Started

### Installation

```bash  
curl -fsSL https://get.pnpm.io/install.sh | sh -
pnpm env use --global lts

git clone https://github.com/tanlab-bit/okto-ui.git
cd okto-ui
```  

### Running the Development Server

Run the development server with the following command:

```bash  
pnpm run dev  
```  

Open your browser and navigate to [http://localhost:3000](http://localhost:3000) to view the application.

### Lint
```basr
pnpm run lint
pnpm run lint:fix
```

### Build for Production

To build the project for production:

```bash  
pnpm run build  
```  

Start the production server:

```bash  
pnpm run start  
```  

### Deploy

Deploy your static site using Nuxt's static generation:

```bash  
pnpm run generate  
```  

## Folder Structure

- `pages/`: Houses application pages, automatically configured for routing.
- `layouts/`: Defines the main layout for the app.
- `composables/`: Contains reusable logic, similar to Vue's `src/layout/composables`.
- `assets/`: Holds static assets such as styles and images.
- `nuxt.config.js`: Centralized configuration file for Nuxt.

## Customization

### Menu
The main menu is defined in the `layouts/AppMenu.vue` file. Update the `model` property to customize menu items.

## Contribution
Contributions are welcome! Feel free to fork the repository, submit issues, or create pull requests.  

## Source

https://github.com/suprimpoudel/sakai-nuxt