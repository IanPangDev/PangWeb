document.addEventListener('DOMContentLoaded', function() {
    const categoryLinks = document.querySelectorAll('.category-filter');
    const projectContainer = document.getElementById('project-container');

    categoryLinks.forEach(link => {
        link.addEventListener('click', function(event) {
            event.preventDefault();
            const category = this.getAttribute('data-category');

            fetchProjects(category);
        });
    });

    function fetchProjects(category) {
        fetch(`/categoria=${category}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok ' + response.statusText);
                }
                return response.json();
            })
            .then(projects => {
                projectContainer.innerHTML = '';

                if (Array.isArray(projects) && projects.length > 0) {
                    projects.forEach(project => {
                        const projectDiv = document.createElement('div');
                        projectDiv.className = 'col-4 col-6-medium col-12-small project';

                        let imageUrl = project.portada ? `/static/images/${project.portada}` : `/static/images/pic00.jpg`;
                        let projectHTML = `
                            <article class="box style2">
                                <a href="${project.path}" class="image featured"><img src="${imageUrl}" alt="" /></a>
                                <h3><a href="${project.path}">${project.titulo}</a></h3>
                                <p>${project.fecha}</p>
                            </article>
                        `;
                        projectDiv.innerHTML = projectHTML;
                        projectContainer.appendChild(projectDiv);
                    });
                } else {
                    projectContainer.innerHTML = '<p><strong>No hay proyectos para esta categoría.</strong></p>';
                }
            })
            .catch(error => {
                console.error('Fetch error: ', error);
                projectContainer.innerHTML = '<p><strong>Error al cargar los proyectos. Intentalo más tarde.</strong></p>';
            });
    }
});