import React from 'react';
import './App.css';
import TableRow from './Components/TableRow/index'
import TableCell from './Components/TableCell/index'

function App() {
  return (
    <table border="1">
        <tbody>
        	<TableRow>
        		<TableCell>This is a test...</TableCell>
                <TableCell>This is a test...</TableCell>
                <TableCell>This is a test...</TableCell>
        	</TableRow>
        </tbody>
    </table>
  );
}

export default App;
