import React from 'react';
import UploadPDF from './UploadPDF';

const App: React.FC = () => {
  return (
    <div className="App">
      <h1 className="text-3xl font-bold p-2 flex flex-col"></h1>
      <UploadPDF />
    </div>
  );
};

export default App;
