using IronPython.Hosting;
using Newtonsoft.Json;
using RestSharp;
using System;
using System.Collections.Generic;
using System.IO;
using System.Text;
using System.Threading.Tasks;

namespace SocialCeo.TweetDownloader {
    public static class Program {
        private static RestClient client = new RestClient("https://api.twitter.com");
        private static string bearerToken = "AAAAAAAAAAAAAAAAAAAAAEau6gAAAAAAp2XOGgBWPnKzlzyDs%2F8zzJQnMzA%3DVMwHnZ3Tx0uKfDDlCswpmjvsE3yuU2kQJYSSl157a4HQpEQps3";

        public static void Main(string[] args) => Run().Wait();

        public static async Task GetToken() {
            var key = "vZJs9n4lvKSjRdMW4Tn97iDr1";
            var secret = "2y4TbG4yH6h2516qnGcNYBuhpeyowP5zlUZPGm94pzn5DYxSL3";

            var bytes = System.Text.Encoding.UTF8.GetBytes(key + ":" + secret);
            var encodedValue = Convert.ToBase64String(bytes);

            var request = new RestRequest("oauth2/token");
            request.AddHeader("Authorization", "Basic " + encodedValue);
            request.AddHeader("Content-Type", "application/x-www-form-urlencoded;charset=UTF-8");
            request.AddQueryParameter("grant_type", "client_credentials");

            var response = await client.ExecutePostTaskAsync(request);

            Console.WriteLine(response.Content);
        }

        public static async Task DownloadTweets() {
            int counter = 16;
            string lastId = null;
            var tweets = new List<JsonTweet>();

            while (counter-- > 0) {
                var request = new RestRequest("1.1/statuses/user_timeline.json");

                request.AddHeader("Authorization", "Bearer " + bearerToken);
                request.AddQueryParameter("screen_name", "elonmusk");
                request.AddQueryParameter("count", "200");
                request.AddQueryParameter("exclude_replies", "false");
                request.AddQueryParameter("trim_user", "true");

                if (lastId != null) {
                    request.AddQueryParameter("max_id", lastId);
                }

                var response = await client.ExecuteGetTaskAsync(request);
                tweets.AddRange(JsonConvert.DeserializeObject<List<JsonTweet>>(response.Content));

                lastId = tweets[tweets.Count - 1].Id;
            }

            var sb = new StringBuilder();
            sb.AppendLine("Date,Retweets,Favorites,Text");

            foreach (var tweet in tweets) {
                sb.Append(tweet.DateCreated.ToShortDateString()).Append(",")
                    .Append(tweet.Retweets).Append(",")
                    .Append(tweet.Favorites).Append(",")
                    .AppendLine(SanitizeTweet(tweet.Text));
            }

            File.WriteAllText("Tweets.csv", sb.ToString());
        }

        public static string SanitizeTweet(string text) {
            return text
                .Replace(",", "")
                .Replace("\n", "")
                .Replace("\r", "");
        }

        public static async Task Run() {
            await DownloadTweets();
        }
    }
}
