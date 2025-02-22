// lint-staged.config.js
module.exports = {
    '**/*.{js,ts,vue}': [
        'pnpm eslint --fix',
    ],
};
