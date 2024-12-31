/** @type {import('./$types').PageServerLoad} */
export async function load({ params }) {
    const res = await fetch(
        `http://localhost:8000/api/recipe/${params.id}`,
    );
    let data = await res.json();

    if (res.ok) {
        return data;
    } else {
        throw new Error(data);
    }
}