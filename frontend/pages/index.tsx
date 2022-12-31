import Head from "next/head";
import { ChangeEvent, useState } from "react";
import useTweetsQuery from "../hooks/tweets";

export default function Tweets() {
  const [tweet, setTweet] = useState("");

  const { tweets, submitTweet, isSubmittingTweet } = useTweetsQuery();

  function handleChange(e: ChangeEvent<HTMLTextAreaElement>): void {
    setTweet(e.target.value);
  }

  function handleSubmit() {
    submitTweet(tweet);
    setTweet("");
  }

  return (
    <div>
      <Head>
        <title>Tweets</title>
      </Head>
      <div>
        <div>
          <h1>Tweets</h1>
          <textarea
            disabled={isSubmittingTweet}
            value={tweet}
            onChange={handleChange}
          />
          <div>
            <button disabled={isSubmittingTweet} onClick={handleSubmit}>
              Submit
            </button>
          </div>
          <div>
            <ul>
              {tweets &&
                tweets.map((tweet) => <li key={tweet.id}>{tweet.text}</li>)}
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}
