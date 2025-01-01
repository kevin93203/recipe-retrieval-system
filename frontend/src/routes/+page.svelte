<script lang="ts">
    import RecipeCard from "../components/RecipeCard.svelte";
    import SearchBox from "../components/SearchBox.svelte";
    import { searchState } from "./shared.svelte.js";

    async function searchByQuery() {
        const formData = new FormData();
        formData.append('query', searchState.query);
        const res = await fetch(`http://localhost:8000/api/search/clip`, {
            method: 'POST',
            body: formData,
        });
        let data = await res.json();

        if (res.ok) {
            return data;
        } else {
            throw new Error(data);
        }
    }

    async function searchByImage(file: File) {
        const formData = new FormData();
        formData.append('file', file);

        const res = await fetch(`http://localhost:8000/api/search/clip`, {
            method: 'POST',
            body: formData,
        });

        let data = await res.json();

        if (res.ok) {
            return data;
        } else {
            throw new Error(data);
        }
    }

    async function handleSearch(query:string) {
        searchState.query = query;
        searchState.results = await searchByQuery();
    }

    async function handleImageUpload(file: File) {
        searchState.results = await searchByImage(file)
    }
</script>

<main>
    <div class="hero">
        <h1>發現美味食譜</h1>
        <p>輸入食材或上傳美食照片，尋找你的下一道佳餚</p>
        <SearchBox {handleSearch} {handleImageUpload} />
    </div>

    <div class="recipe-grid">
        {#each searchState.results as recipe (recipe.id)}
            <RecipeCard {recipe} />
        {/each}
    </div>
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
</style>
