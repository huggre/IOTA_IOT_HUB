import json

#myj = '{"indexationId":"28b286c3b706076bda94965519135b4c1ef8fee9fd3606fdfdb866972007bc6a","accountId":"wallet-account://ebb95a366f63dd247a175488faada95a90f5b140ff6dff4e603248ab5258e7ea","message":{"id":"52f5e6efdfba069153deae92c56e517e75134624eb05dda880f709247ce70524","version":1,"parents":["006f831c9c36dfe3904f56b7af0388519f13fa3b512d61ca91172d0987dc3be8","47360258953c89235b4fb6c50a49d56d5f64564433884ea190bb4ffe389c6a32","85fd50f88543acde476320ebabb3a6a81f177bab610e1995209463d15ac1b304","c7e8f969caf1871ee9678380c77caf61661cdff80f1a3f5adbe07fe514b91258"],"payloadLength":250,"payload":{"type":"Transaction","data":{"essence":{"type":"Regular","data":{"inputs":[{"type":"Utxo","data":{"input":"2a4dbcb2d0ce6ac02f0f8419bf3bc916fd5080b0bbfff5432d57a2d2e34f62210000","metadata":{"transactionId":"2a4dbcb2d0ce6ac02f0f8419bf3bc916fd5080b0bbfff5432d57a2d2e34f6221","messageId":"394534b00bc89fe1ae23706c5fa3c356bdf0aaaa84ddca851367af56315c565e","index":0,"amount":3016667,"isSpent":true,"address":"atoi1qqngum3m7jwgch3cfq00vyptwng4q8llamftz0rnqj6hlspgxf67kuhxpmm","kind":"SignatureLockedSingle"}}}],"outputs":[{"type":"SignatureLockedSingle","data":{"address":"atoi1qza90q34sj4ewku3hqu572p58mnyv5txp4wj8menlk6mxjwc5rlfu5g5pmg","amount":2016667,"remainder":true}},{"type":"SignatureLockedSingle","data":{"address":"atoi1qrj7age88q0lgylh8jwz9tc6nhd040djnn3cvg6kndrgn7055vy6x77sk32","amount":1000000,"remainder":false}}],"payload":{"type":"Indexation","data":{"index":[102,105,114,101,102,108,121],"data":[]}},"internal":false,"incoming":true,"value":1000000,"remainderValue":2016667}},"unlock_blocks":[{"type":"Signature","data":{"type":"Ed25519","data":{"public_key":[234,251,85,86,61,137,142,221,212,242,31,40,215,53,109,159,5,253,222,252,45,27,200,208,245,249,158,4,233,216,149,205],"signature":[224,47,185,84,142,57,51,41,98,132,180,67,47,25,49,22,119,106,93,250,89,242,86,119,125,206,234,12,87,96,131,185,125,251,126,176,87,204,85,23,43,136,43,42,49,158,235,34,155,128,54,124,6,34,226,62,172,103,191,24,69,109,86,8]}}}]}},"timestamp":"2021-05-04T10:42:51Z","nonce":13835058055282304488,"confirmed":true,"broadcasted":true,"reattachmentMessageId":null}}'

myj = '{"indexationId":"4e9caca74c82855ed665f4ae4e002c25971a8a432ec84615bd30ed37f4b77324","accountId":"wallet-account://ebb95a366f63dd247a175488faada95a90f5b140ff6dff4e603248ab5258e7ea","message":{"id":"0efcc73c0f595416415c6c13f5474780c26ce3978894b34699119a99cceb7d91","version":1,"parents":["4490922bb59d998166545deaeedd8fbd8fc04d61dbb21eb1d4590a6314f00200","4aabbbd8d6442e197911541ba1ebb47227a4a1771efbe3b9c4c5668d6743962b","a95e09a03d8f3c0fb23701f292186ed7d4e4b65a97638d5efd0b307ef5fd6a57","c5d98d4da172de04b4873c4a3c863518f2b6b228e6441eeea772608a23de0800"],"payloadLength":250,"payload":{"type":"Transaction","data":{"essence":{"type":"Regular","data":{"inputs":[{"type":"Utxo","data":{"input":"91ccf4f56bc417a682320f162dbb657c8cbe3fcad13bc8d8b53aad387fc3e5860000","metadata":{"transactionId":"91ccf4f56bc417a682320f162dbb657c8cbe3fcad13bc8d8b53aad387fc3e586","messageId":"e347fca1290ff89e6ef60b4ebc98c56dce3f02d3cc0b23b04c28b5daf668226c","index":0,"amount":10000000,"isSpent":true,"address":"atoi1qqs2nah6w8az2caxzahmvp2tp32mtprr6asdld9u57esuekf8awf54hpk48","kind":"SignatureLockedSingle"}}}],"outputs":[{"type":"SignatureLockedSingle","data":{"address":"atoi1qqs46sa55vsp2vkzgj5vugd4n5vvcf47xalj2324lp7a3cyetc7mkx276dv","amount":2000000,"remainder":false}},{"type":"SignatureLockedSingle","data":{"address":"atoi1qzveray3w9l2u87da5c438t2qud3jk600ezh7sepqknlwkk72v7p2gewg5l","amount":8000000,"remainder":true}}],"payload":{"type":"Indexation","data":{"index":[102,105,114,101,102,108,121],"data":[]}},"internal":false,"incoming":true,"value":2000000,"remainderValue":8000000}},"unlock_blocks":[{"type":"Signature","data":{"type":"Ed25519","data":{"public_key":[79,188,131,122,87,72,155,33,249,155,228,199,11,226,142,18,162,66,31,107,30,28,230,250,131,83,177,29,138,248,51,62],"signature":[53,115,205,155,217,223,97,108,159,194,173,214,238,54,110,218,92,180,95,20,247,211,24,210,116,238,59,21,199,214,112,240,43,153,119,20,195,182,31,231,231,121,248,162,241,31,31,104,189,251,116,196,61,37,119,223,17,104,184,199,163,172,221,8]}}}]}},"timestamp":"2021-05-05T08:10:01Z","nonce":4611686018428126153,"confirmed":true,"broadcasted":true,"reattachmentMessageId":null}}'

test = json.loads(myj)

message_id = (test['message']['id'])

customer_addr = (test['message']['payload']['data']['essence']['data']['inputs'][0]['data']['metadata']['address'])

asset_addr = (test['message']['payload']['data']['essence']['data']['outputs'][0]['data']['address'])

amount = (test['message']['payload']['data']['essence']['data']['outputs'][0]['data']['amount'])

confirmed = (test['message']['confirmed'])


print('message_id=' + message_id)
print('customer=' + customer_addr)
print('asset=' + asset_addr)
print('amount=' + str(amount))
print('confirmed=' + str(confirmed))


