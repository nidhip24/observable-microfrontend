export function SubscriberForm() {
  return (
    <form
      onSubmit={async (event) => {
        event.preventDefault();
        const formData = new FormData(event.target);
        const formObject = Object.fromEntries(formData.entries());

        try {
          const response = await fetch('https://super-duper-space-zebra-gxj465wx7jghvp64-5002.app.github.dev/email', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify(formObject),
          });

          if (response.ok) {
            const responseData = await response.json();
            if (responseData.status_code === 401) {
              console.error('Error: Unauthorized access -', responseData.message || 'Authentication required');
            } else {
              console.log('Email sent successfully');
            }
          } else {
            console.error('Failed to send email');
          }
        } catch (error) {
          console.error('Error:', error);
        }
      }}
    >
      <label>
        name
        <input name="name" placeholder="your name" />
      </label>
      <label>
        email
        <input name="email" placeholder="your email address" />
      </label>
      <label>
        subject
        <select name="subject">
          <option value="consulting">consulting</option>
          <option value="support">support</option>
        </select>
      </label>
      <label>
        message
        <textarea placeholder="enter your query here" name="message"></textarea>
      </label>
      <button type="submit">Send</button>
    </form>
  );
}