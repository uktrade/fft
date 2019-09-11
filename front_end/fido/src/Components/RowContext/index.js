import React from 'react'

const RowContext = React.createContext({})

export const RowProvider = RowContext.Provider
export const RowConsumer = RowContext.Consumer
export default RowContext
