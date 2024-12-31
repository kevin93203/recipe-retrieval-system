<script lang="ts">
    import { Clock, ChefHat, ArrowLeft, Users, Printer } from "lucide-svelte";
    import { goto } from "$app/navigation";

    let { data } = $props();
</script>

<div class="recipe-detail">
    <div class="content-container">
        <nav class="navigation">
            <button class="back-btn" onclick={() => goto("/")}>
                <ArrowLeft size={20} />
                <span>返回搜尋</span>
            </button>

            <button class="print-btn" onclick={() => window.print()}>
                <Printer size={20} />
                <span class="hide-mobile">列印食譜</span>
            </button>
        </nav>

        <div class="hero">
            <div class="hero-image">
                <img src={data.image} alt={data.name} />
            </div>
            <div class="hero-content">
                <div class="title-section">
                    <h1>{data.name}</h1>
                    <p class="description">{data.description}</p>

                    <div class="hashtags">
                        {#each data.hashtags as tag}
                            <span class="hashtag">#{tag}</span>
                        {/each}
                    </div>
                </div>

                <div class="meta-info">
                    <div class="meta-item">
                        <Clock size={18} />
                        <span>{data.duration}</span>
                    </div>
                    <div class="meta-item">
                        <ChefHat size={18} />
                        <span>{data.difficulty}</span>
                    </div>
                    <div class="meta-item">
                        <Users size={18} />
                        <span>{data.servings}</span>
                    </div>
                </div>
            </div>
        </div>

        <div class="recipe-content">
            <aside class="ingredients-sidebar">
                <div class="ingredients-container">
                    <h2>食材準備</h2>
                    <div class="ingredients-list">
                        {#each data.ingredients as ingredient}
                            <div class="ingredient-item">
                                <span class="ingredient-name"
                                    >{ingredient.name}</span
                                >
                                <span class="ingredient-amount"
                                    >{ingredient.amount}</span
                                >
                            </div>
                        {/each}
                    </div>
                </div>
            </aside>

            <main class="steps-content">
                <h2>製作步驟</h2>
                <div class="steps-list">
                    {#each data.steps as step}
                        <div class="step-item">
                            <div class="step-header">
                                <div class="step-number">{step.id}</div>
                                <h3>步驟 {step.id}</h3>
                            </div>

                            <div class="step-content">
                                <div class="step-image">
                                    <img
                                        src={step.image}
                                        alt={`步驟 ${step.id}`}
                                    />
                                </div>

                                <div class="step-text">
                                    <p class="step-description">
                                        {step.description}
                                    </p>
                                    {#if step.tips}
                                        <div class="step-tips">
                                            <strong>小提醒：</strong>
                                            <p>{step.tips}</p>
                                        </div>
                                    {/if}
                                </div>
                            </div>
                        </div>
                    {/each}
                </div>
            </main>
        </div>
    </div>
</div>

<style lang="scss">
    .recipe-detail {
        min-height: 100vh;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1rem;

        @media (min-width: 768px) {
            padding: 2rem;
        }
    }

    .content-container {
        max-width: 1440px;
        margin: 0 auto;
    }

    .navigation {
        display: flex;
        justify-content: space-between;
        margin-bottom: 2rem;

        button {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.8rem 1.2rem;
            background: white;
            border: none;
            border-radius: 12px;
            cursor: pointer;
            font-weight: 500;
            transition: all 0.2s;

            &:hover {
                transform: translateY(-2px);
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            }
        }

        .print-btn {
            background: #f8f9fa;

            @media print {
                display: none;
            }
        }
    }

    .hero {
        background: white;
        border-radius: 24px;
        overflow: hidden;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.1);
        margin-bottom: 2rem;

        @media (min-width: 1024px) {
            display: grid;
            grid-template-columns: 1fr 1fr;
            min-height: 400px;
        }
    }

    .hero-image {
        height: 300px;

        @media (min-width: 1024px) {
            height: 100%;
        }

        img {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }
    }

    .hero-content {
        padding: 2rem;

        @media (min-width: 1024px) {
            padding: 3rem;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }
    }

    .title-section {
        margin-bottom: 2rem;

        h1 {
            margin: 0 0 1rem;
            font-size: clamp(1.8rem, 4vw, 2.5rem);
            background: linear-gradient(45deg, #ff512f, #dd2476);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .description {
            font-size: clamp(1rem, 2vw, 1.2rem);
            color: #666;
            line-height: 1.6;
        }
    }

    .meta-info {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
        gap: 1.5rem;

        .meta-item {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            color: #666;
        }
    }

    .recipe-content {
        display: grid;
        gap: 2rem;

        @media (min-width: 1024px) {
            grid-template-columns: 300px 1fr;
        }

        @media (min-width: 1200px) {
            grid-template-columns: 350px 1fr;
        }
    }

    .ingredients-sidebar {
        .ingredients-container {
            background: white;
            border-radius: 24px;
            padding: 2rem;
            box-shadow: 0 8px 32px rgba(31, 38, 135, 0.1);

            @media (min-width: 1024px) {
                position: sticky;
                top: 2rem;
            }
        }

        h2 {
            margin: 0 0 1.5rem;
            font-size: 1.5rem;
            color: #333;
        }
    }

    .ingredients-list {
        display: grid;
        gap: 1rem;

        .ingredient-item {
            display: flex;
            justify-content: space-between;
            padding: 1rem;
            background: #f8f9fa;
            border-radius: 12px;

            .ingredient-amount {
                color: #666;
                font-weight: 500;
            }
        }
    }

    .steps-content {
        h2 {
            margin: 0 0 2rem;
            font-size: 1.8rem;
            color: #333;
        }
    }

    .steps-list {
        display: flex;
        flex-direction: column;
        gap: 3rem;
    }

    .step-item {
        background: white;
        border-radius: 24px;
        padding: 2rem;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.1);
    }

    .step-header {
        display: flex;
        align-items: center;
        gap: 1rem;
        margin-bottom: 1.5rem;

        .step-number {
            width: 40px;
            height: 40px;
            background: linear-gradient(45deg, #ff512f, #dd2476);
            color: white;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
        }

        h3 {
            margin: 0;
            font-size: 1.3rem;
            color: #333;
        }
    }

    .step-content {
        display: grid;
        gap: 2rem;

        @media (min-width: 768px) {
            grid-template-columns: 1fr 1fr;
        }
    }

    .step-image {
        img {
            width: 100%;
            height: 250px;
            object-fit: cover;
            border-radius: 16px;
        }
    }

    .step-text {
        .step-description {
            font-size: 1.1rem;
            line-height: 1.6;
            color: #444;
            margin: 0 0 1rem;
        }

        .step-tips {
            background: #fff8e1;
            padding: 1rem;
            border-radius: 12px;

            strong {
                color: #f4a261;
            }

            p {
                margin: 0.5rem 0 0;
                color: #666;
            }
        }
    }

    @media (max-width: 767px) {
        .hide-mobile {
            display: none;
        }

        .step-content {
            grid-template-columns: 1fr;
        }

        .step-image img {
            height: 200px;
        }
    }

    @media print {
        .recipe-detail {
            background: white;
            padding: 0;
        }

        .navigation {
            display: none;
        }

        .recipe-content {
            grid-template-columns: 1fr;
        }

        .step-item {
            break-inside: avoid;
            box-shadow: none;
        }
    }

    .hashtags {
        display: flex;
        flex-wrap: wrap;
        gap: 0.8rem;
        margin-top: 1.5rem;
    }

    .hashtag {
        display: inline-block;
        padding: 0.4rem 1rem;
        background: rgba(255, 81, 47, 0.1);
        color: #ff512f;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 500;
        transition: all 0.2s ease;

        &:hover {
            background: rgba(255, 81, 47, 0.2);
            transform: translateY(-2px);
        }
    }

    @media (max-width: 768px) {
        .hashtags {
            gap: 0.6rem;
        }

        .hashtag {
            padding: 0.3rem 0.8rem;
            font-size: 0.8rem;
        }
    }
</style>
