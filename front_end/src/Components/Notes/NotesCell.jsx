import React, { useState } from "react";
import { getURLSegment, postJsonData } from "../../Util";

const Modal = ({ isOpen, notes, employee_no, onClose, onSave }) => {
  const [currentNotes, setCurrentNotes] = useState(notes);

  if (!isOpen) return null;

  const handleSubmit = async (e) => {
    e.preventDefault();
    const financialYear = getURLSegment(0);
    const costCentre = getURLSegment(1);
    const response = await postJsonData(
      `/payroll/api/${costCentre}/${financialYear}/employees/notes`,
      {
        employee_no,
        notes: currentNotes,
      },
    );
    console.log(response.status);
    if (response.status === 204) {
      onSave(currentNotes);
      onClose();
    }
  };

  return (
    <div className="govuk-modal-overlay">
      <div className="govuk-modal">
        <div className="govuk-modal__header">
          <h2 className="govuk-heading-m">
            {notes ? "Edit Notes" : "Add Notes"}
          </h2>
        </div>
        <div className="govuk-modal__header">
          <span className="govuk-description">
            Notes will be reset at the end of the {getURLSegment(0)} financial
            year
          </span>
        </div>
        <form onSubmit={handleSubmit}>
          <div className="govuk-form-group">
            <label className="govuk-label" htmlFor="notes">
              Notes
            </label>
            <textarea
              id="notes"
              value={currentNotes}
              onChange={(e) => setCurrentNotes(e.target.value)}
              className="govuk-textarea"
              rows="5"
            />
          </div>
          <div className="govuk-button-group">
            <button
              type="submit"
              className="govuk-button"
              data-module="govuk-button"
            >
              Save
            </button>
            <button
              type="button"
              onClick={onClose}
              className="govuk-button govuk-button--secondary"
              data-module="govuk-button"
            >
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

const NotesCell = ({ notes = "", employee_no }) => {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [currentNotes, setCurrentNotes] = useState(notes);

  const handleSave = (newNotes) => {
    setCurrentNotes(newNotes);
    console.log("handeling modal close");
  };
  return (
    <>
      <a
        href="#"
        title={currentNotes}
        className="govuk-link"
        onClick={(e) => {
          e.preventDefault();
          setIsModalOpen(true);
        }}
      >
        {currentNotes ? "Edit Notes" : "Add Notes"}
      </a>

      <Modal
        isOpen={isModalOpen}
        notes={currentNotes}
        employee_no={employee_no}
        onClose={() => setIsModalOpen(false)}
        onSave={handleSave}
      />
    </>
  );
};

export default NotesCell;
