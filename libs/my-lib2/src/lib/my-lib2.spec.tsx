import React from 'react';
import { render } from '@testing-library/react';

import MyLib2 from './my-lib2';

describe(' MyLib2', () => {
  it('should render successfully', () => {
    const { baseElement } = render(<MyLib2 />);
    expect(baseElement).toBeTruthy();
  });
});
