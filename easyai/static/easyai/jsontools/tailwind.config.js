module.exports = {
  content: [
    "../../../templates/easyai/base/*.{html,js}",
    "../../../templates/easyai/common/*.{html,js}",
    "../../../templates/easyai/easy/*.{html,js}",
    "../../../templates/easyai/full/*.{html,js}",
    "../../../templates/easyai/prediction/*.{html,js}",
    "../js/*.{html,js}"
  ],
  theme: {
    extend: {},
    boxShadow: {
      lg: '0 10px 15px -3px rgba(60, 60, 60, 30%), 0 4px 6px -2px rgba(60, 60, 60, 15%)'
    },
    minHeight: {
      '80': '20rem',
    }    
  },
  plugins: [],
}
