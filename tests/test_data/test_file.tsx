// @ts-ignore
import React from 'react';
// @ts-ignore
import styled from 'styled-components';

const Container = styled.div`
  background-color: #F8F8F8;
  color: #4A4A4A;
`;

const Button = styled.button`
  background-color: #F8F8F8;
  border: 1px solid #4A4A4A;
  color: #4A4A4A;
`;

const TestComponent: React.FC = () => {
  return (
    <Container>
      <h1>Hello, world!</h1>
      <Button>Click Me</Button>
    </Container>
  );
};

export default TestComponent;
