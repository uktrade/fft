import React, { useState } from "react";
import { getURLSegment, postJsonData } from "../../Util";
import ErrorSummary from "../Common/ErrorSummary";

const Modal = ({ section, isOpen, notes, id, onClose, onSave }) => {
  const charLimit = 200;
  const errorMsg =
    "There’s a problem with the system it can’t save this note, try again later.";
  const currentLimit = charLimit - (notes?.length || 0);
  const [currentNotes, setCurrentNotes] = useState(notes || "");
  const [charLeft, setCharLeft] = useState(currentLimit);
  const [errorMessage, setErrorMessage] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const financialYear = String(window.financialYear);
  const costCentre = String(window.costCentreCode);

  if (!isOpen) return null;

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    setErrorMessage("");

    try {
      const response = await postJsonData(
        `/payroll/api/${costCentre}/${financialYear}/${section}/notes`,
        {
          id,
          notes: currentNotes,
        },
      );

      if (response.status >= 200 && response.status < 300) {
        onSave(currentNotes, id);
        onClose();
      } else {
        setErrorMessage(errorMsg);
      }
    } catch (error) {
      console.error("Error saving notes:", error);
      setErrorMessage(errorMsg);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleTextChange = (e) => {
    setCurrentNotes(e.target.value);
    setCharLeft(charLimit - e.target.value.length);
  };

  const isExceeded = charLeft < 0;
  const formGroupClasses = `govuk-form-group ${errorMessage ? "govuk-form-group--error" : ""}`;

  return (
    <dialog className="govuk-modal-dialog" aria-labelledby="modal-title" open>
      <div className="govuk-modal-overlay">
        <div className="govuk-modal">
          <div className="govuk-modal__header">
            <h2 className="govuk-heading-m" id="modal-title">
              {notes ? "Edit note" : "Add note"}
            </h2>
            <span className="govuk-hint">
              Notes will be reset at the end of the {financialYear} financial
              year
            </span>
          </div>

          <form onSubmit={handleSubmit} noValidate>
            {errorMessage && (
              <ErrorSummary errors={[{ message: errorMessage, label: "" }]} />
            )}

            <div className={formGroupClasses}>
              <div
                className="govuk-character-count"
                data-module="govuk-character-count"
                data-maxlength={charLimit}
              >
                <div className="govuk-form-group">
                  <label className="govuk-label" htmlFor="notes">
                    Notes
                  </label>
                  {isExceeded && (
                    <p id="notes-error" className="govuk-error-message">
                      <span className="govuk-visually-hidden">Error:</span>{" "}
                      Notes must be {charLimit} characters or fewer
                    </p>
                  )}
                  <textarea
                    className={`govuk-textarea govuk-js-character-count ${isExceeded ? "govuk-textarea--error" : ""}`}
                    id="notes"
                    name="notes"
                    rows="5"
                    aria-describedby="notes-hint notes-info"
                    value={currentNotes}
                    onChange={handleTextChange}
                    maxLength={charLimit}
                  />
                </div>
                <div
                  id="notes-info"
                  className={`govuk-hint govuk-character-count__message ${isExceeded ? "govuk-error-message" : ""}`}
                  aria-live="polite"
                >
                  You have {charLeft} characters remaining
                </div>
              </div>
            </div>

            <div className="govuk-button-group">
              <button
                type="submit"
                className="govuk-button"
                data-module="govuk-button"
                disabled={isSubmitting || isExceeded}
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
    </dialog>
  );
};

const NotesCell = ({ notes = "", id, section, onSave }) => {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [currentNotes, setCurrentNotes] = useState(notes);

  const handleSave = (updatedNote, id) => {
    setCurrentNotes(updatedNote);
    onSave(updatedNote, id);
  };

  return (
    <>
      <a
        href="#"
        title={currentNotes}
        className="govuk-link govuk-link--no-visited-state "
        onClick={(e) => {
          e.preventDefault();
          setIsModalOpen(true);
        }}
      >
        {currentNotes ? "Edit note" : "Add note"}
      </a>
      <span className="truncate govuk-!-margin-left-3">{currentNotes}</span>
      <Modal
        isOpen={isModalOpen}
        notes={currentNotes}
        id={id}
        section={section}
        onClose={() => setIsModalOpen(false)}
        onSave={handleSave}
      />
    </>
  );
};

export default NotesCell;
