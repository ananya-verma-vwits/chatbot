import { createGlobalStyle } from 'styled-components';

export const GlobalStyles = createGlobalStyle`
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

body {
    background: ${({ theme }) => theme.body};
    color: ${({ theme }) => theme.text};
    transition: all 0.50s linear;
    margin: 0;
    padding: 0;
    font-family: 'Inter', sans-serif;
  }

  .app {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
  }

  header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 20px 0;
  }

  button {
    transition: all 0.3s ease;
    &:hover {
      opacity: 0.8;
    }
  }
`;