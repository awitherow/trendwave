import { useMutation, useQuery } from "react-query";

type Tweet = {
  id: number;
  text: string;
};

export default function useTweetsQuery() {
  const { data: tweets } = useQuery<Tweet[], Error>("tweets", async () => {
    try {
      return await (
        await fetch(`${process.env.NEXT_PUBLIC_API_URL}/tweets/`)
      ).json();
    } catch (error: any) {
      throw new Error("Error fetching tweets");
    }
  });

  const { mutate: submitTweet, isLoading: isSubmittingTweet } = useMutation(
    async (tweet: string) => {
      try {
        const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/tweets/`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            text: tweet,
            approved: false,
          }),
        });
        const json = await res.json();
        return json;
      } catch (error: any) {
        throw new Error("Error creating tweet");
      }
    }
  );

  return {
    tweets,
    submitTweet,
    isSubmittingTweet,
  };
}
