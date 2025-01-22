import * as React from "react";

import {
  Table,
  Header,
  HeaderRow,
  Body,
  Row,
  HeaderCell,
  Cell,
} from "@table-library/react-table-library/table";
import { useTheme } from "@table-library/react-table-library/theme";
import { getTheme } from "@table-library/react-table-library/baseline";
import { months, monthsToTitleCase } from "../../Util";
import { useState } from "react";

export const TableTest = () => {
  const nodes = [
    {
      id: "0",
      name: "John Smith",
      grade: "Grade 7",
      employee_no: "00000001",
      fte: 1.0,
      programme_code: 338887,
      budget_type: "DEL",
      assignment_status: "Active Assignment",
      apr: true,
      may: true,
      jun: false,
      jul: false,
      aug: false,
      sep: false,
      oct: false,
      nov: false,
      dec: false,
      jan: false,
      feb: false,
      mar: false,
    },
  ];
  const initialData = { nodes };
  const [data, setData] = useState(initialData);

  const theme = useTheme(getTheme());

  const [hiddenColumns, setHiddenColumns] = useState([]);

  const toggleColumn = (column) => {
    if (hiddenColumns.includes(column)) {
      setHiddenColumns(hiddenColumns.filter((v) => v !== column));
    } else {
      setHiddenColumns(hiddenColumns.concat(column));
    }
  };

  function handleCheckboxChange(rowId, month) {
    setData((prevData) => ({
      nodes: prevData.nodes.map((node) => {
        if (node.id === rowId) {
          console.log("here");
          const startIndex = months.indexOf(month);
          const toggleValue = !node[month];
          const newNode = { ...node };
          months.slice(startIndex).forEach((m) => {
            newNode[m] = toggleValue;
          });
          return newNode;
        }
        return node;
      }),
    }));
  }

  const handleUpdate = (value, id, property) => {
    setData((state) => ({
      ...state,
      nodes: state.nodes.map((node) => {
        if (node.id === id) {
          return { ...node, [property]: value };
        } else {
          return node;
        }
      }),
    }));
  };

  return (
    <>
      <div>
        <label htmlFor="assignment_status">
          <input
            id="assignment_status"
            type="checkbox"
            value="ASSIGNMENT_STATUS"
            checked={!hiddenColumns.includes("ASSIGNMENT_STATUS")}
            onChange={() => toggleColumn("ASSIGNMENT_STATUS")}
          />
          Assignment status
        </label>
      </div>
      <Table data={data} theme={theme}>
        {(rows) => (
          <>
            <Header>
              <HeaderRow>
                <HeaderCell>Name</HeaderCell>
                <HeaderCell>Grade</HeaderCell>
                <HeaderCell>Employee No</HeaderCell>
                <HeaderCell>FTE</HeaderCell>
                <HeaderCell>Programme code</HeaderCell>
                <HeaderCell>Budget type</HeaderCell>
                <HeaderCell hide={hiddenColumns.includes("ASSIGNMENT_STATUS")}>
                  Assignment status
                </HeaderCell>
                {monthsToTitleCase.map((month) => (
                  <HeaderCell key={month}>{month}</HeaderCell>
                ))}
              </HeaderRow>
            </Header>

            <Body>
              {rows.map((item) => (
                <Row key={item.id} item={item}>
                  <Cell>
                    <input
                      type="text"
                      style={{
                        width: "100%",
                        border: "none",
                        fontSize: "1rem",
                        padding: 0,
                        margin: 0,
                      }}
                      value={item.name}
                      onChange={(event) =>
                        handleUpdate(event.target.value, item.id, "name")
                      }
                    />
                  </Cell>
                  <Cell>{item.grade}</Cell>
                  <Cell>{item.employee_no}</Cell>
                  <Cell>{item.fte}</Cell>
                  <Cell>{item.programme_code}</Cell>
                  <Cell>{item.budget_type}</Cell>
                  <Cell hide={hiddenColumns.includes("ASSIGNMENT_STATUS")}>
                    {item.assignment_status}
                  </Cell>
                  {months.map((month) => (
                    <Cell key={month}>
                      <input
                        type="checkbox"
                        checked={item[month]}
                        onChange={() => handleCheckboxChange(item.id, month)}
                      />
                    </Cell>
                  ))}
                </Row>
              ))}
            </Body>
          </>
        )}
      </Table>
    </>
  );
};
