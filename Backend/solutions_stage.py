# %%
# !pip install faiss-cpu
# !pip install sentence-transformers

# %%
import pandas as pd
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import time
# %%
csv_file_path = 'solutions_similarity_dump/preprocessed_solutions_v1.csv'
df = pd.read_csv(csv_file_path)

# %%
df['preprocessed_solution'] = df['preprocessed_solution'].str.replace('\n', ' ')
df['preprocessed_solution'] = df['preprocessed_solution'].str.replace('\r', ' ')
df = df.drop_duplicates(subset=['solution', 'preprocessed_solution'])
df = df.dropna(subset=['solution', 'preprocessed_solution'])
# %%
code_snippets = df['preprocessed_solution'].tolist()

# %%
# !pip install voyageai

# %%
import os
import voyageai

os.environ['VOYAGE_API_KEY'] = "YOUR_VOYAGE"
vo = voyageai.Client(api_key=os.environ.get("VOYAGE_API_KEY"))

# %%
class CodeSearch:
    def __init__(self, code_snippets, dataframe):
        self.code_snippets = code_snippets
        self.df = dataframe
        self.embedding_model = None
        self.index = None
        self.codes_embeddings = None
        self.dim = 0
        self.do_embedding()

    def do_embedding(self):
        batch_size = 32
        self.code_embeddings = []

        for i in range(0, len(code_snippets), batch_size):
            print(f"batch #{i} begins")
            batch = code_snippets[i:i + batch_size]
            self.code_embeddings += vo.embed(
                batch, model="voyage-code-2", input_type="document"
            ).embeddings
            print(f"batch #{i} finished successfully")
            time.sleep(0.1)

        self.codes_embeddings = np.array(self.code_embeddings, dtype=float)
        self.dim = self.codes_embeddings.shape[1]  # Dimension of the embeddings
        print(f"Dimensions = {self.dim}")
        self.index = faiss.IndexFlatIP(self.dim)  # Use a FlatIP index for inner product (cosine similarity)
        self.index.add(self.codes_embeddings)  # Add the embeddings to the index
    
    def save_faiss_index(self, file_path="solutions_similarity_dump/faiss_index.bin"):
        faiss.write_index(self.index, file_path)
        
    def query(self, query_code, k=10):
        query_embedding = np.array(vo.embed([query_code], model="voyage-code-2", input_type="query").embeddings, dtype=float)
        D, I = self.index.search(query_embedding, k)  # D: distances, I: indices
        print("Top similar problems:")
        for i, idx in enumerate(I[0]):
            print(f"{i+1}: {self.df['solution'].iloc[idx]} {self.df['problem_link'].iloc[idx]} (Similarity: {D[0][i]})")

# %%
search_engine = CodeSearch(code_snippets, df)

# %%
search_engine.save_faiss_index()

# %%
import re

def remove_comments(code):
    # Remove single line & multi-line comments
    regex = '\/\/.*|\/\*(\S|\s)*\*\/'
    code = re.sub(regex, '', code)
    return code

def remove_directives_and_namespace(code):
    # Remove the include directives
    code = re.sub(r'#include.*', '', code)
    # Remove the using namespace
    code = re.sub(r'using namespace.*', '', code)
    return code

def remove_non_ascii(code):
    return code.encode('ascii', 'ignore').decode('ascii')

def clean_code(code):
    if code:
        return code.replace('\n', ' ').replace('\r', ' ')

# Preprocess query
def preprocess_query(code):
    code = remove_comments(code)
    code = remove_non_ascii(code)
    code = remove_directives_and_namespace(code)
    code = clean_code(code)
    return code

# %%
query = """
#include <bits/stdc++.h>
using namespace std;
typedef long long ll;
const int mod = 1e9 + 7;
const int N = 1e5 + 5;

void testCase()
{
    int n, u, v, root = 0;
    ll ans = LLONG_MAX;

    cin >> n;

    vector<int> color(n);
    vector<vector<int>> cost(3, vector<int>(n));
    vector<vector<int>> adj(n);

    for (int i = 0; i < 3; ++i)
    {
        for (auto &c : cost[i])
            cin >> c;
    }

    for (int i = 0; i < n - 1; ++i)
    {
        cin >> u >> v;
        u--, v--;
        adj[u].push_back(v);
        adj[v].push_back(u);
    }

    for (int i = 0; i < n; ++i)
    {
        if ((int)adj[i].size() > 2)
            return void(cout << "-1");
        if (adj[i].size() == 1)
            root = i;
    }

    vector<int> perm = {0, 1, 2};

    function<ll(int, int, int)> dfs = [&](int u, int par, int ind)
    {
        ll ans = cost[perm[ind]][u];
        for (auto v : adj[u])
        {
            if (v != par)
                ans += dfs(v, u, (ind + 1) % 3);
        }
        return ans;
    };

    function<void(int, int, int)> dfs_ans = [&](int u, int par, int ind)
    {
        color[u] = perm[ind];
        for (auto v : adj[u])
        {
            if (v != par)
                dfs_ans(v, u, (ind + 1) % 3);
        }
    };
    do
    {
        ll ret = dfs(root, root, 0);
        if (ret < ans)
        {
            ans = ret;
            dfs_ans(root, root, 0);
        }
    } while (next_permutation(perm.begin(), perm.end()));

    cout << ans << '\n';
    for (int i = 0; i < n; ++i)
        cout << color[i] + 1 << ' ';
}

signed main()
{
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);

    int testCases = 1;

    // cin >> testCases;

    while (testCases--)
        testCase();

    return 0;
}
"""

# %%
# preprocessed_query = preprocess_query(query)

# %%
search_engine.query(query, k=5)  # Retrieve top 5 similar problems


