# Experiment Analytics Project

This project contains the code required to create the analytics dashboard for experiments, blocks, users, sessions, and so on. It consists of several typescript files that initialize charts for their respective analytics dashboard pages.

## Getting started

### Requirements

- Node.js

### Installation & running

1. Navigate to the directory of the project

```bash
cd backend/experiment/static/analytics
```

2. Install dependencies

This will install all the dependencies required to run the project. At the moment of writing, these dependencies are:
- `nodemon`: A utility that will monitor for any changes in your source and automatically restart your server.
- `typescript`: A language that builds on JavaScript by adding static type definitions.

```bash
npm install
```

3. Watch & rebuild the typescript files

This will start a nodemon process that rebuilds the typescript files whenever they are changed.

```bash
npm run dev
```

4. Build the typescript files

This will build the typescript files into javascript files.

```bash
npm run build
```
