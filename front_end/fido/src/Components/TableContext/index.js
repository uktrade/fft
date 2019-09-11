import React from 'react'

const TableContext = React.createContext({})

export const TableProvider = TableContext.Provider
export const TableConsumer = TableContext.Consumer
export default TableContext
