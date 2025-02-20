import { useNavigate, useParams } from 'react-router-dom';
import QuestionForm from '../components/QuestionForm';
import useFetch from '../hooks/useFetch';
import { createQuestionAPIUrl } from '../config';
import { QuestionData } from '../types/types';
import useBoundStore from '../utils/store';
import { useState } from 'react';

const emptyFormData = {
  key: '',
  question: '',
  type: 'text',
  options: [],
  required: false,
  index: 0,
};

function QuestionFormPage() {
  // Extract the question id (if editing)
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const addToast = useBoundStore(state => state.addToast);

  // Only fetch if id exists
  const url = id ? createQuestionAPIUrl(`questions/${id}`) : '';
  const [data, error, loading] = id ? useFetch<QuestionData>(url) : [emptyFormData, null, false];
  const [submitError, setSubmitError] = useState<{ [key: string]: string } | null>(null);

  const handleSubmit = async (submittedData: QuestionData) => {

    setSubmitError(null);

    const url = id ? createQuestionAPIUrl(`questions/${id}`) : createQuestionAPIUrl('questions');
    const method = id ? 'PUT' : 'POST';

    const requestOptions = {
      method,
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${localStorage.getItem('jwt')}`,
      },
      body: JSON.stringify(submittedData),
    };

    const response = await fetch(url, requestOptions);
    const json = await response.json();

    if (!response.ok) {

      const message = "Something went wrong. Please try again.";
      setSubmitError(json);

      addToast({ message, level: 'error', duration: 3000 });
      return;
    }

    addToast({ message: 'Question saved successfully!', level: 'success', duration: 3000 });

    if (!id && json.id) {
      navigate(`/questions/${json.id}`);
      return;
    }
  };

  if (id && loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;

  if (id && !data) return <div>No data found.</div>;
  if (id && data) {
    data.key = id;
  }

  return (
    <div className="p-4">
      <h2 className="text-2xl font-bold mb-4">{id ? 'Edit Question' : 'New Question'}</h2>
      <QuestionForm initialData={id ? data : emptyFormData} onSubmit={handleSubmit} error={submitError} />
    </div>
  );
}

export default QuestionFormPage;
