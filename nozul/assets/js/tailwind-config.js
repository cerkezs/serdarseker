tailwind.config = {
  theme: {
    extend: {
      colors: {
        primary: { DEFAULT:'#ff7a2d', 600:'#f06b1c', 50:'#fff3eb' },
        ink: '#0f1115',
        surface: '#f7f7f8',
      },
      fontFamily: {
        sans: ['Inter','ui-sans-serif','system-ui','sans-serif'],
        display: ['"Space Grotesk"','ui-sans-serif','system-ui','sans-serif'],
      },
      boxShadow: {
        soft: '0 6px 20px -10px rgba(15,17,21,0.18)',
        elegant: '0 24px 48px -16px rgba(255,122,45,0.35)',
      },
      backgroundImage: {
        'gradient-primary': 'linear-gradient(135deg,#ff7a2d 0%,#ff9a55 100%)',
        'gradient-hero': 'linear-gradient(135deg,#0f1115 0%,#1a1d24 60%,#262932 100%)',
      },
    }
  }
}