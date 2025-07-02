use reqwest::Client;
use serde::{Deserialize, Serialize};

#[derive(Debug, Deserialize, Serialize, Clone)]
#[serde(rename_all = "camelCase")]
struct InnerData {
    year: i32,
    price: f32,
    
    #[serde(rename = "CPU model")]
    cpu: String,

    #[serde(rename = "Hard disk size")]
    hard_disk: String,
}

#[derive(Debug, Deserialize, Serialize, Clone)]
#[serde(rename_all = "camelCase")]
struct Data {
    id: String,
    name: String,
    data: InnerData,
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let url = "https://api.restful-api.dev/objects/7";
    let client = Client::new();

    let body: Data = client
        .get(url)
        .send()
        .await?
        .json()
        .await?;

    println!("{:#?}", body);

    Ok(())
}
