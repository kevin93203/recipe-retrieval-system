<script lang="ts">
    import RecipeCard from "../components/RecipeCard.svelte";
    import SearchBox from "../components/SearchBox.svelte";
    import { searchState } from './shared.svelte.js';
    
    async function getData() {
        const res = await fetch(
            `http://10.54.12.187:8000/api/search?query=${searchState.query}`,
        );
        let data = await res.json();

        if (res.ok) {
            return data;
        } else {
            throw new Error(data);
        }
    }

    const mockRecipes = [
        {
            id: 1,
            name: "蒜蓉炒青菜",
            description: "簡單美味的快炒青菜,清爽開胃",
            image: "https://imageproxy.icook.network/fit?background=255%2C255%2C255&height=800&nocrop=false&stripmeta=true&type=auto&url=http%3A%2F%2Ftokyo-kitchen.icook.tw.s3.amazonaws.com%2Fuploads%2Frecipe%2Fcover%2F471124%2Fe04e96b619c43007.jpg&width=800",
            duration: "15分鐘",
            difficulty: "簡單",
            ingredients: [
                { name: "青江菜", amount: "300克" },
                { name: "蒜末", amount: "2湯匙" },
                { name: "鹽", amount: "適量" },
                { name: "食用油", amount: "2湯匙" },
            ],
            steps: [
                {
                    id: 1,
                    description: "青江菜洗淨切段",
                    image: "/images/step1.jpg",
                },
                {
                    id: 2,
                    description: "蒜末爆香",
                    image: "/images/step2.jpg",
                },
                {
                    id: 3,
                    description: "加入青江菜快炒",
                    image: "/images/step3.jpg",
                },
                {
                    id: 4,
                    description: "加入適量鹽調味即可",
                    image: "/images/step4.jpg",
                },
            ],
        },
        // ... 其他食譜數據
    ];

    async function handleSearch(query) {
        searchState.query = query;
        searchState.results = await getData()
        console.log(searchState.results)
        // searchState.results = mockRecipes.filter(
        //     (recipe) =>
        //         recipe.name.includes(query) ||
        //         recipe.description.includes(query),
        // );
    }

    async function handleImageUpload(event) {
        const file = event.detail;
        searchState.results = mockRecipes;
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
