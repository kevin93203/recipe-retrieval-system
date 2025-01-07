<script lang="ts">
    import RecipeCard from "../components/RecipeCard.svelte";
    import SearchBox from "../components/SearchBox.svelte";
    import { searchState } from "./shared.svelte.js";

    let updateKey = 0;

    // 在需要強制更新時呼叫這個函數
    function forceUpdate() {
        updateKey += 1;
    }

    async function searchByQuery() {
        let url = "";
        if (searchState.type === "recipe") {
            url = `http://localhost:8000/api/search?query=${searchState.query}&top_k=12`;
        } else {
            url = `http://localhost:8000/api/ingredient-search?ingredients=${searchState.query}&top_k=12`;
            console.log(url);
        }
        const res = await fetch(url);
        let data = await res.json();

        if (res.ok) {
            return data;
        } else {
            throw new Error(data);
        }
    }

    async function searchByImage(selectedFile: File, imageSearchTerm: string) {
        const formData = new FormData();
        formData.append("file", selectedFile);

        const res = await fetch(
            `http://localhost:8000/api/multimodal-search?top_k=12&text=${imageSearchTerm}`,
            {
                method: "POST",
                body: formData,
            },
        );

        let data = await res.json();

        if (res.ok) {
            return data;
        } else {
            throw new Error(data);
        }
    }

    async function handleSearch(query: string) {
        searchState.query = query;
        searchState.results = await searchByQuery();
        forceUpdate(); // 加在這裡
    }

    async function handleImageUpload(selectedFile: File, imageSearchTerm: string) {
        searchState.results = await searchByImage(selectedFile, imageSearchTerm);
        forceUpdate(); // 加在這裡
    }
</script>

<main>
    <div class="hero">
        <h1>發現美味食譜</h1>
        <p>輸入食材或上傳美食照片，尋找你的下一道佳餚</p>
        <SearchBox {handleSearch} {handleImageUpload} />
    </div>

    {#if searchState.results.length === 0 && searchState.query !== null}
        <div class="empty-state">
            <div class="empty-message">
                <h2>找不到相關食譜☹️</h2>
                <p>
                    {#if searchState.type === "recipe"}
                        試試使用不同的關鍵字，或更改搜尋方式
                    {:else}
                        試試使用其他食材組合，或更改搜尋方式
                    {/if}
                </p>
            </div>
        </div>
    {:else}
        <div class="recipe-grid">
            {#each searchState.results as recipe (recipe.id + "-" + updateKey)}
                <RecipeCard {recipe} />
            {/each}
        </div>
    {/if}
</main>

<style lang="scss">
    main {
        min-height: 100vh;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }

    .hero {
        text-align: center;
        padding: 4rem 2rem;
        background: linear-gradient(
            rgba(255, 255, 255, 0.9),
            rgba(255, 255, 255, 0.95)
        );
        margin-bottom: 3rem;

        h1 {
            font-size: 2.5rem;
            margin: 0 0 1rem;
            background: linear-gradient(45deg, #ff512f, #dd2476);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: bold;
        }

        p {
            font-size: 1.2rem;
            color: #666;
            margin-bottom: 2rem;
        }
    }

    .recipe-grid {
        max-width: 1200px;
        margin: 0 auto;
        padding: 0 2rem;
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
        gap: 2rem;
        padding-bottom: 4rem;
    }

    .empty-state {
        max-width: 1200px;
        margin: 0 auto;
        padding: 4rem 2rem;
    }

    .empty-message {
        backdrop-filter: blur(10px);
        border-radius: 16px;
        padding: 3rem;
        text-align: center;

        h2 {
            font-size: 1.5rem;
            color: #333;
            margin: 0 0 1rem;
        }

        p {
            color: #666;
            font-size: 1.1rem;
            margin: 0;
        }
    }
</style>
