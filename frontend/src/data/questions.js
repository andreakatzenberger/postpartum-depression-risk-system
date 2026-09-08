/**
 * Sva pitanja iz upitnika na jednom mestu.
 *
 * `id`     - mora se poklapati sa nazivom polja u UpitnikInput (api/schemas.py)
 * `value`  - mora biti TACNA vrednost koju backend ocekuje (Literal tipovi)
 * `label`  - ono sto korisnica vidi (na engleskom - vidljivo u UI)
 *
 * Ako se jednog dana promeni skup podataka (npr. predje se na faktore
 * rizika), menja se SAMO ovaj fajl - komponente ostaju netaknute.
 */

/**
 * Pitanje koje se postavlja SAMO u režimu prikupljanja podataka (anketa),
 * i to kao prvo. Odgovor se na backendu upisuje u kolonu `feeling_depressed`
 * - to je ciljna promenljiva koju model uči da predviđa. Ovo je pitanje
 * o SAMOPROCENI (isti pristup kao kolona "Feeling anxious" u Kaggle skupu),
 * a ne o lekarskoj dijagnozi.
 */
export const SELF_ASSESSMENT_QUESTION = {
  id: 'feels_depressed',
  section: 'Self-assessment',
  label: 'Do you feel depressed?',
  help: 'This is a self-assessment, not a clinical diagnosis.',
  options: [
    { value: 'no', label: 'No' },
    { value: 'yes', label: 'Yes' },
  ],
}

export const QUESTIONS = [
  {
    id: 'age',
    section: 'About you',
    label: 'How old are you?',
    help: 'Select the range you fall into.',
    options: [
      { value: '25-30', label: '25 – 30' },
      { value: '30-35', label: '30 – 35' },
      { value: '35-40', label: '35 – 40' },
      { value: '40-45', label: '40 – 45' },
      { value: '45-50', label: '45 – 50' },
    ],
  },
  {
    id: 'feeling_sad',
    section: 'Mood',
    label: 'Do you feel sad or tearful?',
    help: 'Think about the past few weeks.',
    options: [
      { value: 'no', label: 'No' },
      { value: 'sometimes', label: 'Sometimes' },
      { value: 'yes', label: 'Yes' },
    ],
  },
  {
    id: 'irritable',
    section: 'Mood',
    label: 'Are you irritable toward the baby or your partner?',
    help: 'A feeling of tension, nervousness, or anger without a clear reason.',
    options: [
      { value: 'no', label: 'No' },
      { value: 'sometimes', label: 'Sometimes' },
      { value: 'yes', label: 'Yes' },
    ],
  },
  {
    id: 'trouble_sleeping',
    section: 'Daily life',
    label: 'Do you have trouble sleeping at night?',
    help: 'Not counting waking up because of the baby.',
    options: [
      { value: 'no', label: 'No' },
      { value: 'two or more days a week', label: 'Two or more days a week' },
      { value: 'yes', label: 'Yes' },
    ],
  },
  {
    id: 'concentration_problems',
    section: 'Daily life',
    label: 'Do you have difficulty concentrating or making decisions?',
    help: 'For example, it is hard to follow a conversation or finish something you started.',
    options: [
      { value: 'no', label: 'No' },
      { value: 'often', label: 'Often' },
      { value: 'yes', label: 'Yes' },
    ],
  },
  {
    id: 'appetite_problems',
    section: 'Daily life',
    label: 'Have you noticed changes in your appetite?',
    help: 'Overeating or loss of appetite compared to before.',
    options: [
      { value: 'no', label: 'No' },
      { value: 'yes', label: 'Yes' },
    ],
  },
  {
    id: 'guilt',
    section: 'Feelings',
    label: 'Do you feel guilty?',
    help: 'A feeling that you are not good enough or that you have let someone down.',
    options: [
      { value: 'no', label: 'No' },
      { value: 'maybe', label: 'Maybe' },
      { value: 'yes', label: 'Yes' },
    ],
  },
  {
    id: 'bonding_problems',
    section: 'Feelings',
    label: 'Do you have difficulty bonding with your baby?',
    help: 'A feeling of distance or lack of closeness.',
    options: [
      { value: 'no', label: 'No' },
      { value: 'sometimes', label: 'Sometimes' },
      { value: 'yes', label: 'Yes' },
    ],
  },
  {
    id: 'suicide_attempt',
    section: 'Feelings',
    label: 'Have you had thoughts of harming yourself?',
    help: 'This question is sensitive. If it is difficult, you may choose to skip it.',
    sensitive: true,
    options: [
      { value: 'no', label: 'No' },
      { value: 'not interested to say', label: 'Prefer not to say' },
      { value: 'yes', label: 'Yes' },
    ],
  },
]
