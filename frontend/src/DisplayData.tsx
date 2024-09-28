import React from 'react';

interface DisplayDataProps {
  data: { nouns: string[]; verbs: string[] } | null;
}

const DisplayData: React.FC<DisplayDataProps> = ({ data }) => {
  if (!data) return null;

  console.log('Displaying data:', data); // Log data when it's being rendered

  return (
    <div className="mt-4">
      <h2>Extracted Data:</h2>
      <p><strong>Nouns:</strong> {data.nouns.join(', ')}</p>
      <p><strong>Verbs:</strong> {data.verbs.join(', ')}</p>
    </div>
  );
};

export default DisplayData;
