# Developing with Angular: Detailed Instructions

## Step 1. Install everything

    sudo apt-get install nodejs
    sudo apt-get install npm

Create a symbolic link for `node`, as many Node.js tools use this name to execute.

    sudo ln /usr/bin/nodejs /usr/bin/node

Verify that you are running node `v4.x.x` or higher and npm `3.x.x` or higher. Older versions produce errors.

    node -v
    npm -v

Install [angular-cli](https://github.com/angular/angular-cli) globally (using `-g` flag).

    npm install -g angular-cli

## Step 2. Understand the workflow

Adding components. This command creates files and updates `app.module.ts`.

    ng generate component new-component

Serving app for development.

    ng serve --host 0.0.0.0 --port 4201

Building bundles for production.

    ng build --prod --aot

