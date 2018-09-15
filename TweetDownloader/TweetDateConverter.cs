using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using System.Globalization;

namespace SocialCeo.TweetDownloader {
    public class TweetDateConverter : JsonConverter<DateTime> {
        public override DateTime ReadJson(JsonReader reader, Type objectType, DateTime existingValue, bool hasExistingValue, JsonSerializer serializer) {
            string date = JToken.Load(reader).ToString();
            var result = DateTime.ParseExact(date, @"ddd MMM dd HH:mm:ss K yyyy", CultureInfo.InvariantCulture);

            return result.ToUniversalTime();
        }

        public override void WriteJson(JsonWriter writer, DateTime value, JsonSerializer serializer) {
            throw new Exception();
        }
    }
}
