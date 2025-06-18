import styled, { keyframes } from 'styled-components';

const dotAnimation = keyframes`
  0%, 80%, 100% { opacity: 0; }
  40% { opacity: 1; }
`;

const DotsContainer = styled.div`
  display: inline-flex;
  align-items: center;
  gap: 4px;
`;

const Dot = styled.span`
  width: 6px;
  height: 6px;
  background: ${({ theme }) => theme.text};
  border-radius: 50%;
  display: inline-block;
  animation: ${dotAnimation} 1.4s infinite ease-in-out both;
  
  &:nth-child(1) { animation-delay: -0.32s; }
  &:nth-child(2) { animation-delay: -0.16s; }
`;

const LoadingDots = () => (
  <DotsContainer>
    <Dot />
    <Dot />
    <Dot />
  </DotsContainer>
);

export default LoadingDots;