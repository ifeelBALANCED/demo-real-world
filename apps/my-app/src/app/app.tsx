import React from 'react';
import * as myLib from "@second/my-lib";

import './app.css';

import { ReactComponent as Logo } from './logo.svg';
import star from './star.svg';

export const App = () => {
  /*
   * Replace the elements below with your own.
   *
   * Note: The corresponding styles are in the ./app.css file.
   */
  // const tag = ;

  return (
    <div className="app">
      <header className="flex">
        <h1>Welcome to my-application!greate</h1>
        <myLib.MyLib />
      </header>
    </div>
  );
};

export default App;
