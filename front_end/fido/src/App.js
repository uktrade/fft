import React, {Fragment, useState, useEffect, useRef } from 'react';
import './App.css';
import { Provider } from 'react-redux';
import { persistor, store } from './Store';
import { PersistGate } from 'redux-persist/integration/react';
import TableRow from './Components/TableRow/index'
import TableCell from './Components/TableCell/index'
import TableHandle from './Components/TableHandle/index'
import { TableProvider } from  './Components/TableContext'

function App() {
    const [mouseIsDown, setMouseIsDown] = useState(false);

    useEffect(() => {
        const captureMouseDn = (e) => {
            console.log("Mouse down", mouseIsDown);
            setMouseIsDown(true);
        }

        const captureMouseUp = (e) => {
            console.log("Mouse up", mouseIsDown);

            setMouseIsDown(false);
        }


        //const setFromEvent = e => setPosition({ x: e.clientX, y: e.clientY });

        document.addEventListener("mousedown", captureMouseDn);
        document.addEventListener("mouseup", captureMouseUp);

        return () => {
            document.removeEventListener("onmouseup", captureMouseDn);
            document.removeEventListener("mousedown", captureMouseUp);
        };
    }, []);

    return (
        <Provider store={store}>
            <PersistGate loading={null} persistor={persistor}>
                <TableProvider value={{ mouseIsDown: mouseIsDown }}>
                    <table border="1">
                        <tbody>
                        	<TableRow index="0">
                                <TableHandle />
                        		<TableCell cellId="1">This is a test...</TableCell>
                                <TableCell cellId="2">This is a test...</TableCell>
                                <TableCell cellId="3">This is a test...</TableCell>
                        	</TableRow>
                            <TableRow index="1">
                                <TableHandle />
                                <TableCell cellId="4">This is a test...</TableCell>
                                <TableCell cellId="5">This is a test...</TableCell>
                                <TableCell cellId="6">This is a test...</TableCell>
                            </TableRow>
                            <TableRow index="2">
                                <TableHandle />
                                <TableCell cellId="7">This is a test...</TableCell>
                                <TableCell cellId="8">This is a test...</TableCell>
                                <TableCell cellId="9">This is a test...</TableCell>
                            </TableRow>
                        </tbody>
                    </table>
                </TableProvider>
            </PersistGate>
        </Provider>
    );
}

export default App;
