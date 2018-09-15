using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.Text;

namespace SocialCeo.TweetDownloader {
    public class JsonTweet {
        [JsonProperty("created_at")]
        [JsonConverter(typeof(TweetDateConverter))]
        public DateTime DateCreated { get; private set; }

        [JsonProperty("text")]
        public string Text { get; private set; }

        [JsonProperty("retweet_count")]
        public int Retweets { get; private set; }

        [JsonProperty("favorite_count")]
        public int Favorites { get; private set; }

        [JsonProperty("id_str")]
        public string Id { get; private set; }
    }
}
