"""
Script that demonstrates how to use the functions in sdg_util.py

Authors:
* Nick Jelicic (Dialogic)
* Tommy van der Vorst (Dialogic)
* Bijan Ranjbar (MyDataExpert)
* Wilfred Mijnhardt (Rotterdam School of Management)

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.
This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with
this program. If not, see <http://www.gnu.org/licenses/>.

"""

import warnings
warnings.filterwarnings('ignore')

from tqdm.autonotebook import tqdm
from sdg_util import *
import pandas as pd
import torch


class SDGModelWrapper:
    def __init__(self):
        #LOAD MODEL
        self.tokenizer = tokenizers.BertWordPieceTokenizer(
            './models/bert-base-uncased-vocab.txt',
            lowercase=True
        )

        model_config = BertConfig.from_pretrained('bert-base-uncased')
        model_config.output_hidden_states = True
        self.model = SDGModel(conf=model_config)
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model.load_state_dict(torch.load('./models/model_2.bin', map_location=self.device, weights_only=False)['model_state_dict'])

        self.model.eval()
        self.model.to(self.device)

    def classify_sdg(self, text):
        sample_data = {
            "text": text
        }

        df = pd.DataFrame()

        for id in sample_data:
            value = sample_data[id]
            df_this_text = process_text(value)
            df_this_text['id'] = id
            df = pd.concat([df,df_this_text]).reset_index(drop=True)

        #INFERENCE
        df['sdg'] = process_list_of_text(df.text, self.model, self.tokenizer, self.device)

        for i in range(17):
            df["sdg_%i"%(i+1)] = df["sdg"].apply(lambda x: x[i])

        df['id_copy'] = df['id']
        df_agg = df.groupby([
                            'id',
                            'error',
                            ]
                        )["id_copy"].count().reset_index().rename({
                            "id_copy": "num_chunks",
                            "error": "parsing_error"
                            }, axis=1)
        df_agg["num_valid_chunks"] = 0
        df_agg["document_top_sdg"] = ""

        for c in SDG_COLS:
            df_agg[c] = 0

        for uuid in tqdm(df.id.unique()):
            df_sdg_smooth = smoothen_sdg_values(df[df.id==uuid][SDG_COLS], window_size=5)
            scores, top_sdg_index, num_valid_chunks = aggregated_sdg_score(df_sdg_smooth, CONFIDENCE_LEVEL=0.5)
            df_agg.loc[df_agg.id==uuid, SDG_COLS] = scores
            df_agg.loc[df_agg.id==uuid, "document_top_sdg"] = SDG_GOALS[top_sdg_index]
            df_agg.loc[df_agg.id==uuid, "num_valid_chunks"] = num_valid_chunks

        return df_agg
