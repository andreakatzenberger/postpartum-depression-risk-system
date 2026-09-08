import { ArrowLeftIcon, ArrowRightIcon } from './Icons'

export default function Questionnaire({
  questions,
  index,
  answers,
  onAnswer,
  onBack,
  onNext,
  submitting,
  finalLabel = 'Show result',
}) {
  const question = questions[index]
  const selected = answers[question.id]
  const isLast = index === questions.length - 1
  const progress = ((index + (selected ? 1 : 0)) / questions.length) * 100

  return (
    <div className="card">
      <div className="progress">
        <div className="progress__meta">
          <span className="progress__section">{question.section}</span>
          <span className="progress__count">
            {index + 1} / {questions.length}
          </span>
        </div>
        <div className="progress__track">
          <div className="progress__fill" style={{ width: `${progress}%` }} />
        </div>
      </div>

      <div className="question" key={question.id}>
        <h2 className="question__label">{question.label}</h2>
        <p className="question__help">{question.help}</p>

        {question.sensitive && (
          <div className="sensitive-note">
            If this is hard to answer, feel free to choose "Prefer not to say".
          </div>
        )}

        <div className="options" role="radiogroup" aria-label={question.label}>
          {question.options.map((option) => (
            <button
              key={option.value}
              className={`option${selected === option.value ? ' option--selected' : ''}`}
              onClick={() => onAnswer(question.id, option.value)}
              type="button"
              role="radio"
              aria-checked={selected === option.value}
            >
              <span className="option__dot" />
              {option.label}
            </button>
          ))}
        </div>

        <div className="nav">
          <button className="btn btn--ghost" onClick={onBack} disabled={submitting} type="button">
            <ArrowLeftIcon />
            Back
          </button>
          <button
            className="btn btn--primary"
            onClick={onNext}
            disabled={!selected || submitting}
            type="button"
          >
            {isLast ? finalLabel : 'Next'}
            <ArrowRightIcon />
          </button>
        </div>
      </div>
    </div>
  )
}
